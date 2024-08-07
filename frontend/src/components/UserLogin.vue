<template>
    <NavigationBar/>
    <div class="login-form-container">
            <h2 class="form-heading">Login</h2>
            
            <b-form class="login-form" @submit="handleLogin()"  v-if="show">
                <b-form-group
                id="input-group-1"
                label="User Name:"
                label-for="input-1"
                >
                <b-form-input
                    id="input-1"
                    v-model="username"
                    type="text"
                    placeholder="Enter User Name"
                    required
                ></b-form-input>
                </b-form-group>
        
                <b-form-group id="input-group-3" label="Your Password:" label-for="input-3">
                <b-form-input
                    id="input-3"
                    type="password"
                    v-model="password"
                    placeholder="Enter Password"
                    required
                ></b-form-input>
                </b-form-group>
        
                <b-button type="submit" variant="primary">Login</b-button>
            </b-form>
            <span>Create new account</span><router-link to="/signup">SignUp</router-link>
            <!-- <b-card class="mt-3" header="Form Data Result">
                <pre class="m-0">{{ form }}</pre>
            </b-card> -->
    </div>
  </template>
  
  <script>
import axios from 'axios'
// import 'vue3-toastify/dist/index.css'
import { toast } from 'vue3-toastify';
import NavigationBar from '../Navbar/NavigationBar.vue';

    export default {
        name: "SignUp",
        components:{NavigationBar},
      data() {
        return {
          
            username: '',
            password: '',
            show: true
        }
      },
      methods: {
        notify(user_role){
            // Show a success toast
                this.$toast.success("Login Successful", {
                "theme": "auto",
                "type": "success",
                "position": "top-center",
                "autoClose": 800,
                "dangerouslyHTMLString": true,
                onClose: () => {
                    if(user_role==='admin')
                    this.$router.push('/admindashboard');
                else
                    this.$router.push('/userdashboard');
                }
              }) 
          },
        async handleLogin(){

            try{
                const response = await axios.post('http://127.0.0.1:8000/login',{
                    username : this.username,
                    password : this.password
                });
                localStorage.setItem('access_token',response.data.access_token);
                localStorage.setItem('user_id',response.data.user_id);
                localStorage.setItem('user_role',response.data.user_role);
                localStorage.setItem('isauthenticated',true);
                if(response.data.user_role==='admin')
                    this.$router.push('/admindashboard');
                else
                    this.$router.push('/userdashboard');
                
                this.notify(response.data.user_role)
              
            }
            catch(error){
                toast.error(error.response.data.error, {
                "theme": "auto",
                "type": "error",
                "position": "top-center",
                "autoClose": 800,
                "dangerouslyHTMLString": true,
                
                })
                console.error(error.response.data)
            }

        }
      }
    }
  </script>

<style>
.login-form-container{
    margin: 20px 0;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;

    width: 100%;
}
.login-form{
    width: 40%;
    border: 1px solid black;
    padding: 60px 40px;
    border-radius: 10px;
}
.form-heading{
    text-align: center;
    font-size: 35px;
}
</style>