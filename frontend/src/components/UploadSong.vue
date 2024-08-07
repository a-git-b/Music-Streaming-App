<template>
    <NavigationBar/>
    <h2 align="center" style="margin-top: 15px;">Upload Song</h2>
    <div class="song-form-container">
         <form class="song-form" @submit.prevent="upload()" >
            
                <div class="song-input">
                    <label for="name">Song Name</label>
                    <input id="name" type="text" name="song_name" v-model="song_name"/>
                </div>
                <div class="song-input">
                    <label for="name">Song Lyrics</label>
                    <textarea id="name" type="text" name="lyrics" rows="5" cols="74 " v-model="lyrics"></textarea>
                </div>
                <div class="song-input">
                    <label for="duration">Song Duration</label>
                    <input id="duration" type="text" name="duration" v-model="duration"/>
                </div>
                <div class="song-input">
                    <label for="genre">Song Genre</label>
                    <input id="genre" type="text" name="genre" v-model="genre"/>
                </div>
                <div class="song-input">
                    <label for="image" >Upload Image</label>
                    <input id="image" type="file" @change="onImageSelected" />
                </div>
                <div class="song-input">
                    <label for="song">Upload song</label>
                    <input id="song" type="file" @change="onSongSelected"/>
                </div>
                <div class="upload-btn">
                    <button  type="submit">Upload</button>
                </div>
                
        </form>
    </div>
        <!-- <div class="signup-form-container">
            <h2 class="form-heading">Upload Song</h2>
            
            <b-form class="signup-form"  v-if="show">
                <b-form-group id="input-group-1" label="Song Name:" label-for="input-1">
                <b-form-input id="input-1" v-model="song_name" type="text" placeholder="Enter Song Name" required></b-form-input>
                </b-form-group> 
                <b-form-group id="input-group-1" label="Song Image:" label-for="input-1">
                    
    <div class="mt-3">Selected file: {{ song_image ? song_image.name : '' }}</div>

                <b-form-file id="input-1" class="mt-3" :state="Boolean(song_image)" v-model="song_image" placeholder="Upload Image" required></b-form-file> 
                </b-form-group>
                <b-form-file
      v-model="song_image"
      :state="Boolean(song_image)"
      placeholder="Choose a file or drop it here..."
      drop-placeholder="Drop file here..."
    ></b-form-file>
                <b-form-group id="input-group-1" label="Song Audio:" label-for="input-1">
                <b-form-file id="input-1" v-model="audio" type="text" placeholder="Upload Audio" required ></b-form-file>
                </b-form-group>
                <b-form-group id="input-group-1" label="Song Lyrics:" label-for="input-1">
                <b-form-textarea id="input-1" v-model="lyrics" placeholder="Enter Song lyrics" required></b-form-textarea>
                </b-form-group>
                <b-form-group id="input-group-1" label="Song Duration:" label-for="input-1">
                <b-form-input id="input-1" v-model="duration" type="text" placeholder="Enter Song duration" required ></b-form-input>
                </b-form-group>

        
                <b-button type="submit" variant="primary">Upload</b-button>
            </b-form>
           
            </div> 
            <div> -->


</template>
<script>
import axios from 'axios'
import NavigationBar from '../Navbar/NavigationBar.vue'

export default{
    components:{NavigationBar},
    props:['album'],
    data(){
        return{
            song_name : null,
            song_image : null,
            audio : null,
            lyrics : null,
            duration : null,
            genre : null,
            show : true,
            album_id:null
            
        }
    },
    methods:{
        onImageSelected(event){
            console.log(event);
            this.song_image =event.target.files[0];
        },
        onSongSelected(event){
            console.log(event);
            this.audio = event.target.files[0];
        },
        async upload(){
            this.album_id = this.$route.params.album_id
            const fd = new FormData();
                    fd.append('song_name',this.song_name);
                    fd.append('song_image',this.song_image);
                    fd.append('audio',this.audio);
                    fd.append('duration',this.duration);
                    fd.append('lyrics',this.lyrics);
                    fd.append('genre',this.genre);
                    fd.append('album_id',this.album_id)
            try{
                
                const response = await axios.post('http://127.0.0.1:8000/uploadsong',fd,{
          headers: {
            'Content-Type': 'multipart/form-data'}    

                });
                
                console.log(response.data);
            }
            catch(error){
                console.log(error.response.data);
            }
        }



    }


}
</script>



<style>
.song-form-container{
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: center;
    margin-top: 15px;
}
.song-form{ 
    padding: 30px;
    width: 50%;
    border: 1px black solid;
    border-radius: 10px;
}
.song-input label{
    font-weight: 600;
    font-size: 18px;
}
.song-input input{
    width: 100%;
    margin-top: 10px;
}
.upload-btn{
    display: flex;
    flex-direction: row;
    justify-content: center;
    width: 100%;
}
.upload-btn button{
    background-color: rgb(26, 137, 227);
    width: 150px;
    height: 40px;
    font-size: 18px;
    border: none;
    margin-top: 20px;
    border-radius: 10px;
    color: white;
    font-weight: 600;
}

</style>