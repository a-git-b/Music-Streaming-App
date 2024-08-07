<template>
    <NavigationBar/>
    <div class="signup-form-container">
            <h2 class="form-heading">SignUp</h2>
            
            <b-form class="signup-form" @submit.prevent="signup"  v-if="show">
                <b-form-group id="input-group-1" label="User Name:" label-for="input-1">
                <b-form-input id="input-1" v-model="username" type="text" placeholder="Enter User Name" requ ></b-form-input>
                </b-form-group>
        
                <b-form-group id="input-group-2" label="Email address:" label-for="input-2" >
                <b-form-input id="input-2" v-model="email" type="email" placeholder="Enter email" required></b-form-input>
                </b-form-group>
        
                <b-form-group id="input-group-3" label="Your Password:" label-for="input-3">
                <b-form-input id="input-3" type="password" v-model="password" placeholder="Enter Password" required></b-form-input>
                </b-form-group>
        
                <b-button type="submit" variant="primary">SignUp</b-button>
            </b-form>
            <span>Already have an account?</span><router-link to="/userlogin">Login</router-link>
            <!-- <b-card class="mt-3" header="Form Data Result">
                <pre class="m-0">{{ form }}</pre>
            </b-card> -->
    </div>
  </template>
  
  <script>
import NavigationBar from '../Navbar/NavigationBar.vue';
import axios from 'axios';
import {toast} from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'
    export default {
      name: "SignUp",
      components:{NavigationBar},
      data() {
        return {
          
            username: '',
            email: '',
            password: '',
          show: true
        }
      },
      methods: {
        async signup(){
                try{
                    const response = await axios.post('http://127.0.0.1:8000/signup',{
                        username:this.username,
                        email : this.email,
                        password : this.password
                    });
                    console.log('Signup successfully',response.data);
                    this.$router.push("/userlogin");
                }
                catch(error){
                  toast.warning(error.response.data.error, {
                    "theme": "auto",
                    "type": "warning",
                    "position": "top-center",
                    "autoClose": 800,
                    "dangerouslyHTMLString": true,
                })
                this.username= '',
                this.email= '',
                this.password= '',
                console.error(error.response.data)

                }
        }
      }
    }
  </script>

<style>
.signup-form-container{
    margin: 20px 0;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;

    width: 100%;
}
.signup-form{
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