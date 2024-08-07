<template>
    <NavigationBar/>
    <ShowSongs :playlistsongs="playlistsongs"/>

</template>
<script>
import axios from 'axios'
import ShowSongs from './ShowPlaylistSongs.vue'
import NavigationBar from '../Navbar/NavigationBar.vue'
export default{
    components :{ShowSongs,NavigationBar},
    props :['album_id','playlist_id'],
    data(){
        return{
            playlistsongs : null,
            isalbum : false,
            isplaylist : false,

        }
    },
    mounted(){
        if(this.album_id){
            this.isalbum = true
            this.fetchAlbumSongs()
            
        }
        if(this.playlist_id){
            this.isplaylist = true
            this.fetchPlaylistSongs()
        }
    },
    methods:{
        async fetchAlbumSongs(){
            if(this.isalbum){
                try{   
                const response = await axios.get('http://127.0.0.1:8000/getsong');
                this.songs = response.data;
                console.log(response.data);
                console.log(this.songs)

                }
                catch(error){
                    console.error(error.response.data)
                }
            }
        },
        

    
    }
}
</script>