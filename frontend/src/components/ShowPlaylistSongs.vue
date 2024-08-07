<template>
    <NavigationBar/>
    <b-nav class="d-flex justify-content-between my-1">
        <h4>Songs</h4>
        <button  type="button" class="btn btn-secondary">Show More</button>
    </b-nav>
    <div class="card-container">
        <div v-for="song in playlistsongs" :key="song.id" class="card">
            <img :src ="'../../'+song.imageUrl" :height=100 class="card-img-top" alt="Song Image"/>
            <div class="card-body ">
                <h5 class="card-title">{{ song.title }}</h5>
                <div class="btn-group" role="group">
                    <button @click="playSong(song.audio)" type="button" class="btn btn-primary">Play</button>
                    <b-button variant="success" @click="pauseSong(song.audio)" type="button" class="btn btn-primary">Pause</b-button>
                    <button @click="viewLyrics(song)" type="button" class="btn btn-secondary">View Lyrics</button>
                    <b-button variant="danger" @click="removeSong(song.id)">Delete</b-button>
                </div>
            </div>
            <audio ref="audioPlayer" :src="song.audio"></audio>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import NavigationBar from '../Navbar/NavigationBar.vue'
export default {
    name:'ShowPlaylistSongs',
    components:{NavigationBar},
    data(){
        return {
            playlistsongs : null,
            playlist_id : null,
            audio : null
        }
    },
    mounted(){
        this.fetchPlaylistSongs();
    },
    methods: {
    playSong(song) {
        this.audio = new Audio('../../'+song); 
        this.audio.play();
    },
    pauseSong(){
        this.audio.pause();
    },
    viewLyrics(song) {
      console.log('Viewing lyrics for:', song.title);
    },
    async fetchPlaylistSongs(){
            try{    
                this.playlist_id = this.$route.params.playlist_id;
                console.log(this.playlist_id)
                const response = await axios.get('http://127.0.0.1:8000/getsongplay/'+this.playlist_id);
                this.playlistsongs = response.data;
                console.log(response.data);
                console.log(this.playlistsongs)

                }
                catch(error){
                    console.error(error.response.data)
                }


        },
    async removeSong(song_id){
        try{
            const response = await axios.delete('http://127.0.0.1:8000/deleteplaylistsong/'+song_id);
            this.fetchPlaylistSongs();
            console.log(response.data);
        }
        catch(error){
            console.error(error.response.data)
        }
    }
  }
}
</script>

<style scoped>
.card-container{
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
}
</style>