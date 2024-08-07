import { createRouter, createWebHistory } from 'vue-router';
import SignUp from './components/SignUp.vue';
import UserLogin from './components/UserLogin.vue';
import UploadSong from './components/UploadSong.vue';
import AdminDashboard from './components/AdminDashboard.vue';
import UserDashboard from './components/UserDashboard.vue';
import ShowPlaylistSongs from './components/ShowPlaylistSongs.vue'
import ShowAlbumSongs from './components/ShowAlbumSongs.vue'
import HomePage from './components/HomePage.vue'
import CreatorAccount from './components/CreatorAccount.vue'
import ShowCreatorSongs from './components/ShowCreatorSongs.vue'
const routes = [
    {
        name: 'HomePage',
        path: '/',
        component: HomePage
    },
    {
        path : '/signup',
        name : 'SignUp',
        component : SignUp,
    },
    {
        path : '/userlogin',
        name : 'UserLogin',
        component : UserLogin,
    },
    {
        path : '/uploadsong/:album_id',
        name : 'UploadSong',
        component : UploadSong,

    },
    {
        path : '/userdashboard',
        name : 'UserDashboard',
        component : UserDashboard,
    },
    {
        path : '/admindashboard',
        name : 'AdminDashboard',
        component : AdminDashboard,
        meta : {isAdmin:true}
    },
    {
        path : '/creator',
        name : 'CreatorAccount',
        component : CreatorAccount,
    },
    {
        path : '/playlistsongs/:playlist_id',
        name : 'ShowPlaylistSongs',
        component : ShowPlaylistSongs,
    },
    {
        path : '/albumsongs/:album_id',
        name : 'AlbumSongs',
        component : ShowAlbumSongs,
    },
    {
        path : '/creatoralbumsongs/:album_id',
        name : 'ShowCreatorSongs',
        component : ShowCreatorSongs,

    }

]
const router = createRouter({
    history : createWebHistory(process.env.BASE_URL),
    routes,
})
router.beforeEach((to,from,next)=>{
    const user_role = localStorage.getItem('user_role')||'user';
    if(to.meta.isAdmin && user_role!=='admin'){
        next({path:'/userlogin',query:{unauthorized:true}});
    }
    else{
        next();
    }
})
export default router