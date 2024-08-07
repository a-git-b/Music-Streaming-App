from flask import Flask,request,make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity,unset_jwt_cookies
from flask_cors import CORS
from flask_restful import Resource,Api
from werkzeug.utils import secure_filename
from flask import jsonify
import os
from flask import send_from_directory
app = Flask(__name__)
CORS(app,origins='*')
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "site.db")}'
app.config['JWT_SECRET_KEY']='MUSIC'
db = SQLAlchemy(app)
jwt=JWTManager(app)

api = Api(app)

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(150),unique=True,nullable=False)
    password = db.Column(db.String(256),nullable=False)
    email = db.Column(db.String(256),nullable=False,default='abc@gmail.com')
    role = db.Column(db.String(256),nullable = False,default='user')
    albums = db.relationship('Album',backref='artist',lazy = True)
    playlists = db.relationship('Playlist',backref='user',lazy = True)
    rating = db.relationship('Rating',backref='user_r',lazy=True)
    
class Album(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.Integer,nullable=False)
    #release_date = db.Column(db.DateTime,default = datetime.now())
    artist_id = db.Column(db.Integer,db.ForeignKey(User.id),nullable=False)
    songs = db.relationship('Song',backref='album',lazy=True)

class Genre(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(256))
    song = db.relationship('Song',backref='genre',lazy=True)   

class Song(db.Model):
    __tablename__ = "song"
    id = db.Column(db.Integer,primary_key=True)
    song_name = db.Column(db.String(100))
    song_image = db.Column(db.String(1000))
    audio = db.Column(db.String(1000))
    lyrics = db.Column(db.String(1000))
    duration=db.Column(db.Integer)
    genre_id = db.Column(db.Integer,db.ForeignKey(Genre.id),nullable=False)
    album_id = db.Column(db.Integer,db.ForeignKey(Album.id),nullable=False)
    rating = db.relationship('Rating',backref='song_r',lazy=True)
    playlists = db.relationship('Playlist',secondary='song_playlist',back_populates='songs')
    


class Playlist(db.Model):
  
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(250))
    user_id = db.Column(db.Integer,db.ForeignKey(User.id),nullable=False)
    songs = db.relationship('Song',secondary='song_playlist',back_populates='playlists')

song_playlist = db.Table('song_playlist',db.Column('song_id',db.Integer,db.ForeignKey(Song.id)),db.Column('playlist_id',db.Integer,db.ForeignKey(Playlist.id)))

   
class Rating(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    score = db.Column(db.Integer)
    user_id = db.Column(db.Integer,db.ForeignKey(User.id),nullable=False)
    song_id = db.Column(db.Integer,db.ForeignKey(Song.id),nullable=False)



with app.app_context():
    db.create_all()
    admin_username = 'admin'
    admin_password = 'admin'
    if not User.query.filter_by(username=admin_username).first():
        hashed_password = generate_password_hash(admin_password, method='pbkdf2:sha256')
        admin_user = User(username=admin_username,password=hashed_password,role='admin')
        db.session.add(admin_user)
        db.session.commit()
@app.route('/')
def home():
    return 'Hello World'
@app.route('/logout',methods=['POST'])
@jwt_required()
def logout():
    resp = make_response(jsonify({'message':'Logged out successfully'}))
    unset_jwt_cookies(resp)
    return {'message':'Logged out successfully'},200

class SignupResource(Resource):
    def post(self):

        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        print(data)

        if User.query.filter_by(username = username ).first():
            return {'error':'Username already exists'},400
        hashed = generate_password_hash(password,method='pbkdf2:sha256')
        new_user = User(username = username, password=hashed,email=email,role='user')
        db.session.add(new_user)
        db.session.commit()
        return {'message':'Signup Succesfully'},201
    def get(self):
        users = User.query.filter_by(role='user').all()
        if users:
            return len(users),200
        else:
            return {'error':'No users available'},400
    def put(self):
        data = request.get_json()
        user_id = data.get('user_id')
        user = User.query.filter_by(id=user_id).first()
        if user:
            user.role = 'creator'
            db.session.commit()
            return {"message":"Registered as creator"},200
        else :
            return {'error':'Cannot be registered'},400




class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password,password):
            access_token = create_access_token(identity={
                'username':user.username
            })
            return {'message':'Login Successful','access_token':access_token,'user_id':user.id,'user_role':user.role},200
        else:
            return {'error':'Invalid Username or Password'},401
    def get(self,user_id=None):
        if user_id is not None:
            user = User.query.filter_by(id=user_id).first()
            if user.role=='creator':
                return True,200
            else:
                return {'error':'Not a creator'},400
        else:
            creators = User.query.filter_by(role='creator').all()
            if creators:
                return len(creators),200
            else:
                return {'error':'No creators available'},400
        
        
        

        


UPLOAD_FOLDER = 'frontend/public'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp3','mp4a','mp4','wav'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class UploadSongResource(Resource):
    def delete(self,song_id):
        if song_id:
            song = Song.query.filter_by(id=song_id).first()
            if song:
                db.session.delete(song)
                del_song_play = song_playlist.delete().where(song_playlist.c.song_id==song.id)
                db.session.execute(del_song_play)
                db.session.commit()
                return {'message':'Song deleted successfully'},201
            else:
                return  {'error':'Song not found'},400


    def get(self,album_id=None):
        if album_id is None :
            songs = Song.query.all()
            songs_list=[{'id':song.id,'title':song.song_name,'imageUrl':song.song_image,'audio':song.audio,'album_id':song.album_id} for song in songs]
            # print(songs_list)
      
            return songs_list,200
        try:
            songs = Song.query.filter_by(album_id=album_id).all()
            songs_list=[{'id':song.id,'title':song.song_name,'imageUrl':song.song_image,'audio':song.audio,'album_id':song.album_id} for song in songs]
            print(songs_list)
        
            return songs_list,200
        except :
            return {'error':'Song not found'},400

    def post(self):
        album_id = request.form['album_id']
        songName = request.form['song_name']
        songImage = request.files['song_image']
        song = request.files['audio']
        lyrics = request.form['lyrics']
        duration = request.form['duration']
        genre_name = request.form['genre']
        genre=Genre.query.filter_by(name=genre_name.lower()).first()
        genre_id = -1
        if genre :
            genre_id = genre.id
        else:
            new_genre = Genre(name=genre_name.lower())
            db.session.add(new_genre)
            db.session.commit()
            genre_id=Genre.query.filter_by(name = genre_name.lower()).first().id
           

        if songImage and allowed_file(songImage.filename) and song and allowed_file(song.filename):
            filename_image = secure_filename(songImage.filename)
            filename_song = secure_filename(song.filename)
            songImage.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_image))
            song.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_song))

            image_url = filename_image
            song_url = filename_song
            new_song = Song(song_name=songName, song_image=image_url, audio=song_url,lyrics=lyrics,duration=duration,genre_id=genre_id,album_id=album_id)
            db.session.add(new_song)
            db.session.commit()

            return {'message': 'Song Uploaded successfully'}, 201
        else:
            return {'error': 'Invalid file format'}, 400


@app.route('/public/<path:filename>')
def serve_public(filename):
    return send_from_directory('frontend/public', filename)

class AlbumResource(Resource):
    def post(self,userId):
        data = request.get_json()
        title = data.get('title')
        artist_id = userId
        if Album.query.filter_by(title=title.lower()).first() : #globally checking for uniqueness of album
            return {'error' : 'This album already exists' },400
        else:
            new_album = Album(title=title.lower(),artist_id=artist_id)
            db.session.add(new_album)
            db.session.commit()
            return {'message':'Album created successfully'},201
    def get(self,userId=None):
        if userId is None:
            albums = Album.query.all()
            album_list = [{'title':album.title,'id':album.id} for album in albums]
            return album_list,200
        else:
            try:
                albums = Album.query.filter_by(artist_id=userId).all()
                album_list = [{'id':album.id,'title':album.title} for album in albums]
                print(album_list)
                return album_list,200
            except:
                return {'error':'Album Not Found'},400
    def put(self,album_id):
        data = request.get_json()
        newtitle = data.get('newtitle')

        existingalbum = Album.query.filter_by(title=newtitle.lower()).first()
        if existingalbum : 
            return {'error':'This album name already exists'},400
        else :
            album = Album.query.filter_by(id=album_id).first()
            if album :
                album.title = newtitle.lower()
                db.session.commit()
                return {'message':'Album name updated successfully'},200
            else:
                return {'error':'Album not found'},400
    def delete(self,album_id):
        if album_id:
            songs = Song.query.filter_by(album_id=album_id).all()
            list_song_ids = [ song.id for song in songs]
            print(list_song_ids)
            # removing song from usersplaylist
            for song_id in list_song_ids:
                song_playlist = SongPlaylistResource()
                song_playlist.delete(song_id)
            # deleting song 
            for song_id in list_song_ids:
                songs_to_delete = UploadSongResource()
                songs_to_delete.delete(song_id)
            # deleting album
            album = Album.query.filter_by(id=album_id).first()
            if album:
                db.session.delete(album)
                db.session.commit()
                return {"message":"Album deleted successfully"},201
            return {"error":"Album cannot be deleted"},400
            
       
class PlaylistResource(Resource):
    def get(self,userId):
        if userId is not None:
            playlists=Playlist.query.filter_by(user_id=userId).all()
            if playlists:
                print(playlists[0].name)
                playlist_list = [{'playlist_id':playlist.id,'name':playlist.name} for playlist in playlists]
                return playlist_list,200
            else:
                return {'error':'No Playlist found'},400

    def post(self,userId=None):
        if userId :
            data = request.get_json()
            name = data.get('name')
            if Playlist.query.filter_by(name = name.lower(), user_id=userId).first():
                return {'error':'This playlist already exists'},400
            else:
                new_playlist = Playlist(name = name.lower(), user_id=userId)
                if new_playlist:
                    db.session.add(new_playlist)
                    db.session.commit()
                    return {'message':'Playlist Created successfully'},201 
                else:
                    return {'error':'Playlist cannot be created'},400
    
    def delete(self,id):
        if id:
            playlist = Playlist.query.filter_by(id=id).first()
            if playlist:
                db.session.delete(playlist)
                del_song_play = song_playlist.delete().where(song_playlist.c.playlist_id==playlist.id)
                db.session.execute(del_song_play)
                db.session.commit()
                return {'message':'Playlist deleted successfully'},200
            else:
                return {'error':'Playlist doesn\'t exist'},400
class SongPlaylistResource(Resource):
    def post(self):
        data = request.get_json()
        playlist_id = data.get('playlist_id')
        song_ids = data.get('song_ids')
        unique_songs=set(song_ids)
        for song in unique_songs:
            add_song_playlist = song_playlist.insert().values(playlist_id=playlist_id,song_id=song)
            db.session.execute(add_song_playlist)
        db.session.commit()
        return 'Songs added to playlist successfully',200
    def get(self,playlist_id):
        if playlist_id:
            songs_in_playlist = db.session.query(song_playlist.c.song_id).filter(song_playlist.c.playlist_id==playlist_id).all()
            song_ids = [song_id for song_id, in songs_in_playlist]
            songs = Song.query.filter(Song.id.in_(song_ids)).all()
            songs_list=[{'id':song.id,'title':song.song_name,'imageUrl':song.song_image,'audio':song.audio} for song in songs]
            return songs_list,200
        

    def delete(self,song_id):
        if song_id:
            del_song = song_playlist.delete().where(song_playlist.c.song_id==song_id)
            if del_song:
                db.session.execute(del_song)
                db.session.commit()
                return {'message':'Song deleted from playlist successfully'},200
        
class GenreResource(Resource):
    def get(self):
        genres = Genre.query.all()
        return len(genres),200

class SearchResource(Resource):
    def post(self):
        print("HELLO")
        data = request.get_json()
        searchsong = data.get('searchtrack')
        print(searchsong)
        songs = Song.query.all()
        print(songs)
        res_song = []
        for song in songs:
            print(song.song_name)
            if song.song_name.lower() == searchsong.lower():
                
                print(song)
                res_song.append(song)
        print(res_song)
        songs_list=[{'id':song.id,'title':song.song_name,'imageUrl':song.song_image,'audio':song.audio} for song in res_song]
        print(songs_list)
        return songs_list,200


api.add_resource(SignupResource,'/signup','/getusers','/register')
api.add_resource(LoginResource,'/login','/creator/<int:user_id>','/getcreators')
api.add_resource(PlaylistResource,'/createplay/<int:userId>','/getplaylist/<int:userId>','/deleteplay/<int:id>')
api.add_resource(SongPlaylistResource,'/addsongplay','/getsongplay/<int:playlist_id>','/deleteplaylistsong/<int:song_id>')
api.add_resource(UploadSongResource,'/uploadsong','/getsong','/getsongalbum/<int:album_id>','/deletesong/<int:song_id>')
api.add_resource(AlbumResource,'/album','/album/<int:userId>','/editalbum/<int:album_id>','/deletealbum/<int:album_id>')
api.add_resource(GenreResource,'/getgenre')
api.add_resource(SearchResource,'/searchsong')


if __name__ == '__main__':
    app.run(port=8000,debug=True)