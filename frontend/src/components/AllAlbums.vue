<template>
    
   
    <b-nav class="d-flex justify-content-between my-1">
        <h4>Albums</h4>
        <!-- <button v-if="iscreator" type="button" class="btn btn-secondary">Show More</button> -->
    </b-nav>
    <div class="card-container" >
        <div v-for="album in albums" :key="album.id" class="card my-card">
            <img :src="'https://live-production.wcms.abc-cdn.net.au/a362273509f7eccdcf362bb73b3b006d?impolicy=wcms_crop_resize&cropH=788&cropW=1400&xPos=0&yPos=0&width=862&height=485'" class="card-img-top" alt="Song Image">
            
            <div class="card-body">
                <h5 class="card-title">{{album.title }}</h5>
                <div class="btn-group" role="group">
                    <button @click="showSongs(album.id)" type="button" class="btn btn-primary">View Songs</button>
                    <!-- <button @click="addSong(album.id)" v-if='iscreator' type="button" class="btn btn-primary">Add Song</button> -->
                    <!-- <b-button @click="showEditAlbum(album.id)">Edit</b-button> -->
                    <!-- <button @click="deleteAlbum(album.id)" v-if='iscreator' type="button" class="btn btn-secondary">Delete Album</button> -->
            
                </div>
            </div>
            
        </div>
        
    </div>
   
    <div class="signup-form-container" v-if="show" >
            <h2 class="form-heading">Edit Album</h2>
            <b-form class="signup-form"   @submit="editAlbum()">
                        <b-form-group id="input-group-1" label="Album title:" label-for="input-1">
                        <b-form-input id="input-1" v-model="newtitle" type="text" placeholder="Enter Title" required></b-form-input>
                        </b-form-group> 
                        <b-button type="submit" variant="primary">Edit</b-button>
            </b-form>
            
    </div>
    
</template>

<script>
import axios from 'axios'
export default {
    name:'AllAlbums',
    props:['albums'],
    data(){
        return{
            show : false,
            album_id : null,
            newtitle :'',
            iscreator : false
        }
    },
    methods: {
    showSongs(album_id) {
        // if(this.iscreator){
        //     this.creator=this.iscreator
        // }
        // console.log(this.creator);
      
        this.$router.push("/albumsongs/"+album_id)
    },
     addSong(album_id){
        console.log(album_id);
        this.$router.push("/uploadsong/"+album_id);
        
    },
    showEditAlbum(album_id){
        this.show = true;
        this.album_id=album_id;

    },
    async editAlbum(){
        try{
            const response = await axios.put('http://127.0.0.1:8000/editalbum/'+this.album_id,{
                newtitle: this.newtitle
            });
            console.log(response.data);
            this.show = false;
            this.album_id = null;

        }
        catch(error){
            console.error(error.response.data);
        }
    }
    // async removeAlbum(album_id){
    //     try{
    //         const response = await this.axios.delete('http://127.0.0.1:8000/deletealbum/'+album_id)
    //     }


    // }
    
  }
}
</script>

<style scoped>
.card-container {
    display: flex;
    flex-wrap: nowrap; /* Prevent wrapping of cards */
    overflow-x: scroll; /* Enable horizontal scrolling */
    padding: 10px; /* Add some padding for spacing */
    margin-bottom: 20px; /* Add margin to the bottom */
}

.my-card {
    flex: 0 0 auto; /* Maintain the width of each card */
    margin-right: 10px; /* Add margin between cards */
    width: 300px; /* Adjust card width as needed */
}


</style>