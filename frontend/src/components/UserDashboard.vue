<template>
    <NavigationBar/>
    <RecommendedTracks :songs="songs" />
    <AllAlbums :albums="albums"/>
    <UserPlaylist :playlists="playlists" :fetchPlaylists="fetchPlaylists"/>
    
</template>

<script>
import axios from 'axios'
import RecommendedTracks from './RecommendedTracks.vue'
import UserPlaylist from './UserPlaylist.vue'
import NavigationBar from '../Navbar/NavigationBar.vue'
import AllAlbums from './AllAlbums.vue'
export default {
    name: "UserDashboard",
    components:{RecommendedTracks,NavigationBar,UserPlaylist,AllAlbums},

    data(){
        return{
            songs : null,
            playlists : null,
            albums : null,
            user_id : null
            
        }

    },
    mounted(){
        this.fetchSongs();
        this.fetchAlbums();
        this.fetchPlaylists();
    },
    methods:{
        async fetchSongs(){
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
        async fetchAlbums(){
            try{
                const response = await axios.get('http://127.0.0.1:8000/album');
                this.albums = response.data;
                console.log(response.data);
                console.log(this.albums);

            }
            catch(error){
                console.error(error.response.data);
            }
            
        },
        async fetchPlaylists(){
            try{
                this.user_id=localStorage.getItem('user_id')
                const response = await axios.get('http://127.0.0.1:8000/getplaylist/'+this.user_id);
                this.playlists=response.data;
                console.log(this.playlists);
            
            }
            catch(error){
                console.error(error.response.data);
            }
        }

    }
}
</script>