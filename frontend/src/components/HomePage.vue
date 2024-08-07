<template>
    <NavigationBar/>
    <div class="homepage">
            <div class="container">
            <h1>Welcome To Music Streaming App</h1>
    </div>
    </div>
    
 </template>
 
 <script>
    import NavigationBar from '../Navbar/NavigationBar.vue'
     export default {
         name:"HomePage",
         components:{NavigationBar}
     }
 </script>
 <style  scoped>
 .homepage{
    width: auto;
    height: 100vh;
    background: #000;
}
 .container {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    color: white;
}

</style>