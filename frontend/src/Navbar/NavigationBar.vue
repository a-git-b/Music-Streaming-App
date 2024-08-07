<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="info">
      <b-navbar-brand href="/userdashboard">Sangeet</b-navbar-brand>
      <b-navbar-nav class="ml-auto">
        <b-nav-form v-if="isauthenticated">
          <b-form-input size="sm" class="mr-sm-2" placeholder="Search"></b-form-input>
          <b-button  size="sm" class="my-2 my-sm-0" type="submit">Search</b-button>
        </b-nav-form>
        <router-link to="/userlogin" v-if=!user_id><b-nav-item>Login</b-nav-item></router-link>
        <router-link to="/signup" v-if=!user_id><b-nav-item>SignUp</b-nav-item></router-link>
        <router-link  to="/creator"><b-nav-item v-if="user_id && user_role!=='admin' ">Creator Account </b-nav-item></router-link>
        <b-nav-item v-if="user_id && user_role!=='admin'">Profile</b-nav-item>
        <b-nav-item v-if="user_id"  @click="logout()">Logout</b-nav-item>
        
      </b-navbar-nav>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
    </b-navbar>
  </div>
</template>

<script>
// import axios from 'axios'
export default {
  name: "NavigationBar",
  data(){
    return {
      user_id : null,
      user_role : null,
      isadmin : false,
      isauthenticated : false
      
    }
  },
  mounted(){
      this.user_id = localStorage.getItem('user_id')
      this.user_role = localStorage.getItem('user_role')
      this.isauthenticated = localStorage.getItem('isauthenticated')

      
      if(this.user_role & this.user_role==='creator'){
        this.isCreator=true
      }
      console.log(this.user_id)
  },
  // watch: {
  //   '$route'() {
      
  //     this.authenticated = localStorage.getItem('isauthenticated') === true
  //     console.log(this.authenticated)
  //   }
  // },
  methods:{
    // logout(){
    //   this.user_id=null
    //   this.user_role=null
    //         const access_token = localStorage.getItem('access_token');
    //         axios.post('http://127.0.0.1:8000/logout',null,{
    //             headers:{
    //                 Authorization: `Bearer ${access_token}`
    //             }
    //     })

    //         .then(()=>{
    //             localStorage.removeItem('access_token');
                
    //             localStorage.removeItem('user_id');
    //             localStorage.removeItem('user_role');
    //             this.user_id=null
    //             this.user_role = 'user'
    //             localStorage.setItem('isauthenticated',false);
    //             this.isauthenticated = false;
    //             this.$router.push('/userlogin')
    //         })
    //     },
    async logout(){
            const access_token = localStorage.getItem('access_token');
            console.log(access_token)
            this.$axios.post('http://127.0.0.1:8000/logout',null,{
                headers:{
                    Authorization: `Bearer ${access_token}`
                }
        })
            .then(()=>{
                localStorage.removeItem('user_id');
                localStorage.removeItem('access_token');
                localStorage.removeItem('user_role');
                localStorage.setItem('isauthenticated',false);
                this.user_id = null;
                this.user_role = null;
                this.$router.push('/userlogin')
            })
        },

        creatorAccount(){

        }

  }
  
}
</script>