<template>
    <b-nav class="d-flex justify-content-between my-1">
        <h4>Your Playlist</h4>
        <a href="#pl-form"><button  @click="showPlaylistForm()" type="button" class="btn btn-secondary" >Create New Playlist</button></a>
        <!-- <button  @click="showPlaylistForm()" type="button" class="btn btn-secondary" >Create New Playlist</button> -->
    </b-nav>
    <div class="card-container">
        <div v-for="playlist in playlists" :key="playlist.id" class="card my-card">
            <img :src="'https://images.unidays.world/i/self-serve/content/offer094b3885-e0f5-4fcf-a835-0a4c6cd503f6'" class="card-img-top" alt="Song Image">
            <div class="card-body ">
                <div class="card-header d-flex justify-content-between">
                    <h5 class="card-title">{{ playlist.name }}</h5>
                    <!-- <font-awesome-icon :icon="['fas', 'trash']" /> -->
                    
                </div>
                
                <div class="btn-group" role="group">
                    <button @click="viewSongs(playlist)" type="button" class="btn btn-primary">View Songs</button>
                    <button @click="showSongForm(playlist)" type="button" class="btn btn-secondary">Add Songs</button>
                    <b-button variant="danger" @click="removePlaylist(playlist.playlist_id)">Delete</b-button>
                </div>
            </div>
        </div>
    </div>
    <!-- <button @click="showForm()" type="button" class="btn btn-primary" v-if="!show">Create Playlist</button> -->
    <div id="pl-form" class="signup-form-container" v-if="showPlaylistform" >
            <h2 class="form-heading">Create Playlist</h2>
            <b-form class="signup-form"   @submit="createPlaylist()">
                        <b-form-group id="input-group-1" label="Playlist name :" label-for="input-1">
                        <b-form-input id="input-1" v-model="name" type="text" placeholder="Enter name" required></b-form-input>
                        </b-form-group> 
                        <b-button type="submit" variant="primary">Create</b-button>
            </b-form>
    </div>
   
    <div class="playlist-form-container" v-if="showAddSong" >
        <h4>Add Songs</h4>

        <div class="playlist-form">

                        <!-- <div class="playlist-header d-flex  justify-content-between">
                            <b-form-group>
                                <b-form-input
                                    id="input-1"
                                    v-model="playlistname"
                                    type="text"
                                    placeholder="Enter playlist name"
                                    required
                                ></b-form-input>
                              </b-form-group>
                            <b-nav-form class="d-flex flex-row align-item-center ">
                                <b-form-input size="sm"  class="mr-sm-2 " placeholder="Search"></b-form-input>
                                <b-button size="sm" class="my-2 my-sm-0" type="submit">Search</b-button>
                            </b-nav-form>
                        </div> -->

                        <!-- <b-form-group id='playlist-1'  
                                v-for="song in songs"
                                v-model="playlist"
                                :key="song.id">
                            <b-form-checkbox value={{song.title}} >{{song.title}}</b-form-checkbox>
                        </b-form-group> -->
                        <div class="checklist-container">
                            <ul class="list-group checklist" v-for="(song) in songs" :key="song.id">
                                <li class="list-group-item">
                                    <input class="checklist-item" type="checkbox" v-model="playlist" :value="song.id">
                                    {{ song.title }}
                                </li>
                            </ul>
                        </div>
                        <b-button type="button" variant="primary" @click="addToPlaylist()">Add</b-button>
            </div>
            </div>
    

</template>

<script>
import axios from 'axios';


export default {
    name:'UserPlaylist',
    props:['playlists','fetchPlaylists'],
    data(){
        return{
            user_id : null,
            showPlaylistform : false,
            showAddSong:false,
            songs : null,
            playlist:[],
            playlistName:'',
            selectedplay:null
            
        }
    },
    methods: {
    showPlaylistForm(){
        this.showPlaylistform = !this.showPlaylistform
    },
    showSongForm(playlist){

        this.showSongs();
        this.selectedplay=playlist.playlist_id;
        this.showAddSong =true;
    },
    viewSongs(playlist) {
      console.log('Playing:', playlist.name);
      this.$router.push("/playlistsongs/"+playlist.playlist_id)
    },
    addSongs(playlist){
        console.log('Playing:', playlist.id);
    },
    async createPlaylist() {
        try{
            this.user_id = localStorage.getItem('user_id');
            const response = await axios.post('http://127.0.0.1:8000/createplay/'+this.user_id,{
                name : this.name
            });
            this.showPlaylistForm();
            this.fetchPlaylists();
            console.log(response.data);

        }
        catch(error){
            console.error(error);
        } 
    },
    async removePlaylist(playlistId){
        try{
            const response = await axios.delete('http://127.0.0.1:8000/deleteplay/'+playlistId);
            this.showSongs()
            console.log(response.data);
        }
        catch(error){
            console.error(error.response.data);
        }
        
       
    },
    async showSongs(){
        try{
                const response = await axios.get('http://127.0.0.1:8000/getsong');
                this.songs = response.data;
                console.log(response.data);
                console.log(this.songs)

            }
            catch(error){
                console.error(error.response.data)
            }
    },
    async addToPlaylist(){
        console.log(this.selectedplay)
        console.log(this.playlist)
        try{
            const response = await axios.post('http://127.0.0.1:8000/addsongplay',{
            playlist_id : this.selectedplay,
            song_ids : this.playlist
            }   
        );  this.showAddSong =false;
            console.log(response.data);
        }
        catch(error){
            console.error(error.response.data)
        }
    }
  }
}
</script>

<style >
/* .card-container{
    margin: 10px;
    display: flex;
    gap: 5px;
    flex-direction: row;
    align-items: center;
    overflow-x: scroll;
    flex-wrap: nowrap;
}
.card {
  width: 18rem;
  margin-bottom: 20px;
} */
.card-container {
    display: flex;
    flex-wrap: nowrap; /* Prevent wrapping of cards */
    overflow-x: auto; /* Enable horizontal scrolling */
    padding: 10px; /* Add some padding for spacing */
    margin-bottom: 20px; /* Add margin to the bottom */
}

.my-card {
    flex: 0 0 auto; /* Maintain the width of each card */
    margin-right: 10px; /* Add margin between cards */
    width: 300px; /* Adjust card width as needed */
}


.playlist-form-container{
    margin: 20px 0;
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
.playlist-form{
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    width: 50%;
    border: solid black 2px;
    border-radius: 10px;
    padding: 20px;
}
.playlist-header{
    width: 100%;
}
.checklist-container{
    width: 100%;
    height: 300px;
    overflow-y: scroll;
}
.checklist{
    width: 100%;
    margin: 10px 0;
    background-color: black;
    color: white;
}

</style>