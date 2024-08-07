<template>
    <NavigationBar/>
    <div v-if="!iscreator">
        <h3>Register as creator</h3>
        <button @click="register()">Register</button>

    </div>
    <div v-if="iscreator">
    <h3>Total Albums {{ no_of_albums }}</h3>
    <CreatorAlbums :albums="albums" />
    <button @click="showForm()" type="button" class="btn btn-primary" v-if="!show">Create Album</button>
    <div class="signup-form-container" v-if="show" >
            <h2 class="form-heading">Create Album</h2>
            <b-form class="signup-form"   @submit="createAlbum()">
                        <b-form-group id="input-group-1" label="Album title:" label-for="input-1">
                        <b-form-input id="input-1" v-model="title" type="text" placeholder="Enter Title" required></b-form-input>
                        </b-form-group> 
                        <b-button type="submit" variant="primary">Create</b-button>
            </b-form>
            
    </div>
    </div>
  </template>


<script>
import axios from 'axios'
import CreatorAlbums from './CreatorAlbums.vue'
import NavigationBar from '../Navbar/NavigationBar.vue'
export default{
    name: "CreatorAccount",
    components: {NavigationBar,CreatorAlbums},
    data(){
        return{
            albums: null,
            user_id: null,
            no_of_albums:0,
            show : false,
            title:null,
            iscreator:false ,
            

        }
    },
    mounted(){
        this.user_id = localStorage.getItem('user_id');
        this.isCreator();

        this.fetchAlbums();
    },
    methods:{
        async isCreator(){
            try{
                console.log(this.user_id)
                const response = await axios.get('http://127.0.0.1:8000/creator/'+this.user_id);
                // console.log(response.data)
                this.iscreator = response.data=== true
                // console.log(this.iscreator)


            }
            catch(error){
                console.error(error.response.data.error)
            }
        },

        async register(){
            try{
                console.log(this.user_id)
                const response = await axios.put('http://127.0.0.1:8000/register',{
                    user_id : this.user_id
                }

            );
                
            console.log(response.data)
            this.isCreator();
            }
            catch(error){
                console.error(error.reponse.data.error)
            }

        },
        showForm(){
            this.show = !this.show
        },
        async fetchAlbums(){
            try{
                
                if(this.user_id){
                    const response = await axios.get('http://127.0.0.1:8000/album/'+this.user_id);
                    this.albums = response.data;
                    this.no_of_albums = this.albums.length
                    console.log(response.data);
                    
                }
                console.log('Albums'+this.albums)

            }
            catch(error){
                console.error(error.response.data)
            }
            
        },
        
        async createAlbum(){
            
            try{
                this.user_id = localStorage.getItem('user_id');
                const response = await axios.post('http://127.0.0.1:8000/album/'+this.user_id,{
                title : this.title
                }
                );
                console.log(response.data)
                this.fetchAlbums();
                this.showForm();
                this.title=null;

            }
            catch(error){
                console.error(error.response.data)
            }

        }
    }
    
}
</script>