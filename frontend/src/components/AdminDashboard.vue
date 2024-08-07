<template>
    <NavigationBar/>
    <!-- <b-list-group>
        <b-list-group-item>Tracks</b-list-group-item>
        <b-list-group-item>Album</b-list-group-item> -->
        <!-- <router-link><b-list-group-item>Tracks</b-list-group-item></router-link>
        <router-link><b-list-group-item>Albums</b-list-group-item></router-link> -->
    <!-- </b-list-group> -->
    <div class="page-color">
    <h2 align="center">Admin Dashboard</h2>
    <div class="admin-dash d-flex flex-row justify-content-around">
        <div class="left">
            <div class="card-container">
                <div class="card">
                    <div class="card-header">Normal Users</div>
                    <div class="card-body">
                        <h2 >{{ users }}</h2>
                    </div>
                </div>
            </div>
            <div class="card-container">
                <div class="card">
                    <div class="card-header">Creators</div>
                    <div class="card-body">
                        <h2>{{ creators }}</h2>
                    </div>
                </div>
            </div>
        </div>
        <div class="left d-flex flex-row">
            <div class="card-container">
                <div class="card">
                    <div class="card-header">Total Songs</div>
                    <div class="card-body">
                        <h2>{{ songs.length }}</h2>
                    </div>
                </div>
            </div>
            <div class="card-container">
                <div class="card">
                    <div class="card-header">Total albums</div>
                    <div class="card-body">
                        <h2 >{{ albums.length }}</h2>
                    </div>
                </div>
            </div>
            <div class="card-container">
                <div class="card">
                    <div class="card-header">Genres</div>
                    <div class="card-body">
                        <h2 >{{ genres }}</h2>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="admin-tracks" v-show="showsearchedsongs">
        <admin-track-header class="d-flex flex-row justify-content-between px-5 py-2">
            <h3>Searched Songs</h3>
            <!-- <b-nav-form>
                <b-form-input size="sm" class="mr-sm-2" placeholder="Search" v-model="searchtrack"></b-form-input>
                <b-button size="sm" class="my-2 my-sm-0" type="button" @click="searchTrack()" >Search</b-button>
            </b-nav-form> -->
        </admin-track-header>
    
            <track-box-body  v-for="song in searchedsongs" :key="song.id" >
            <b-list-group  class="track-list px-5">
                    <b-list-group-item  class="d-flex flex-row justify-content-between">
                        <div class="left">
                            <h5>{{ song.title }}</h5>
                        </div>
                        <div  class="right">
                            <b-button-group >
                                <b-button >Play</b-button>
                                
                            </b-button-group>
                        </div>
                    </b-list-group-item>
                </b-list-group>

                <!-- <b-list-group v-else class="track-list px-5">
                <b-list-group-item  class="d-flex flex-row justify-content-between">
                        <div class="left">
                            <h4>No Song Available in this Album</h4>
                        </div>
                    
                </b-list-group-item>
                </b-list-group> -->
 
            </track-box-body>
        </div>
  
    <div class="admin-tracks" v-show="showtrack">
        
        <admin-track-header class="d-flex flex-row justify-content-between px-5 py-2">
            <h3>All Albums</h3>
            <b-nav-form>
                <b-form-input size="sm" class="mr-sm-2" placeholder="Search" v-model="searchtrack"></b-form-input>
                <b-button size="sm" class="my-2 my-sm-0" type="button" @click="searchTrack()" >Search</b-button>
            </b-nav-form>
        </admin-track-header>
        
        <div class="track-box " v-for="album in albums" :key="album.id" >
            <track-box-header class="d-flex flex-row justify-content-between px-5 pb-2">
                <h4>{{album.title}}</h4>
                <!-- <b-button variant="outline-primary">Show more</b-button> -->
            </track-box-header>
            <track-box-body  v-for="song in songs" :key="song.id" >
                <b-list-group v-if="song.album_id===album.id" class="track-list px-5">
                    <b-list-group-item  class="d-flex flex-row justify-content-between">
                        <div class="left">
                            <h5>{{ song.title }}</h5>
                        </div>
                        <div  class="right">
                            <b-button-group >
                                <b-button>View lyrics</b-button>
                                <b-button variant="danger" @click="deleteSong(song.id)">Delete</b-button>
                            </b-button-group>
                        </div>
                    </b-list-group-item>
                </b-list-group >
                <!-- <b-list-group v-else class="track-list px-5">
                <b-list-group-item  class="d-flex flex-row justify-content-between">
                        <div class="left">
                            <h4>No Song Available in this Album</h4>
                        </div>
                    
                </b-list-group-item>
                </b-list-group> -->
 
            </track-box-body>
        </div>
    </div>
    </div>

</template>

<script>
    import NavigationBar from '../Navbar/NavigationBar.vue'
    import axios from 'axios'
  
    export default {
        name:"AdminDashboard",
        components:{NavigationBar},
        data(){
            return {
                songavailable : false,
                users : 0,
                creators : 0,
                albums : 0,
                genres : 0,
                songs : 0,
                albumsongs : 0,
                showtrack : true,
                searchtrack : '',
                searchedsongs: null,
                showsearchedsongs:false
            
            }
        },
        mounted(){
            this.fetchusers();
            this.fetchcreators();
            this.fetchalbums();
            this.fetchgenres();
            this.fetchsongs();
            this.songavailable = !this.songavailable;
        },
        methods:{
            async fetchusers(){
                try{
                    const response = await axios.get('http://127.0.0.1:8000/getusers');
                    this.users = response.data;
                    console.log(response.data);

                }
                catch(error){
                    console.error(error.response.data.error);
                }

            },
            async fetchcreators(){
                try{
                    const response = await axios.get('http://127.0.0.1:8000/getcreators');
                    this.creators = response.data;
                    console.log(response.data);

                }
                catch(error){
                    console.error(error.response.data.error);
                }

            },
            async fetchalbums(){
                try{
                    const response = await axios.get('http://127.0.0.1:8000/album');
                    this.albums = response.data;
                    console.log(response.data.length);

                }
                catch(error){
                    console.error(error.response.data.error);
                }

            },
            async fetchgenres(){
                try{
                    const response = await axios.get('http://127.0.0.1:8000/getgenre');
                    this.genres = response.data;
                    console.log(response.data);

                }
                catch(error){
                    console.error(error.response.data.error);
                }

            },
            async fetchsongs(){
                try{
                    const response = await axios.get('http://127.0.0.1:8000/getsong');
                    this.songs = response.data;
                    console.log(response.data.length);

                }
                catch(error){
                    console.error(error.response.data.error);
                }

            },
            async searchTrack(){
                try {
                    console.log(this.searchtrack)
                    const response = await axios.post('http://127.0.0.1:8000/searchsong',{
                        searchtrack : this.searchtrack
                    });
                    this.showsearchedsongs = true
                    this.searchedsongs = response.data
                    console.log(response.data);
                }
                catch(error){
                    console.error(error.response.data.error);
                }

            },
            async deleteSong(song_id){
                try{
                    const response = await axios.delete('http://127.0.0.1:8000/deletesong/'+song_id);
                    console.log(response.data);
                    this.fetchalbums();
                    this.fetchgenres();
                    this.fetchsongs();
                }
                catch(error){
                    console.error(error.response.data.error);
                }
            }

        }
    }
</script>

<style scoped>
.card-container {
  margin: 10px;
}
.card {
  width: 18rem;
  margin-bottom: 20px;
  text-align: center;
}
.card-header{
    font-size: 20px;
    font-weight: 600;
}
.page-color{
    background-color: #FFF8DC;
}
h3{
    text-transform: capitalize;
}
h4{
    text-transform: capitalize;
}
h5{
    font-family: 'Courier New', Courier, monospace;
    text-emphasis: inherit;
    text-transform: capitalize;
}
</style>