<template>
    <b-nav class="d-flex justify-content-between my-1">
        <h4>Recommended Songs</h4>
        <!-- <button  type="button" class="btn btn-secondary">Show More</button> -->
    </b-nav>
    <div class="card-container">
        <div v-for="song in songs" :key="song.id" class="card my-card">
            <img :src= song.imageUrl :height=100  class="card-img-top" alt="Song Image" />
            <div class="card-body ">
                <h5 class="card-title">{{ song.title }}</h5>
                <div class="btn-group" role="group">
                  
                    <button @click="playSong(song.audio)" type="button" class="btn btn-primary">Play</button>
                    <b-button variant="success" @click="pauseSong(song.audio)" type="button" class="btn btn-primary">Pause</b-button>
                    <button @click="viewLyrics(song)" type="button" class="btn btn-secondary">View Lyrics</button>
                </div>
            </div>
            
            <audio ref="audioPlayer" :src="song.audio"></audio>
        </div>
    </div>

</template>

<script>

export default {
    name:'RecommendedTracks',
    props:['songs'],
    data(){
      return {
        audio:null
      }

    },
    methods: {
      playSong(song) {
        // console.log(song)
        this.audio = new Audio(song); 
        this.audio.play();
    },
    pauseSong(){
        this.audio.pause();
    },
    
    viewLyrics(song) {
      console.log('Viewing lyrics for:', song.title);
    }
  }
}
</script>

<style scoped>

/* .card-container{
    margin: 10px;
    display: flex;
    gap: 5px;
    flex-direction: row;
    align-items: center;
    overflow-x: scroll;
    flex-wrap: nowrap;
}
.card {
  width: 18rem;
  margin-bottom: 20px;
} */
.card-container {
    display: flex;
    flex-wrap: nowrap; /* Prevent wrapping of cards */
    overflow-x: auto; /* Enable horizontal scrolling */
    padding: 10px; /* Add some padding for spacing */
    margin-bottom: 20px; /* Add margin to the bottom */
}

.my-card {
    flex: 0 0 auto; /* Maintain the width of each card */
    margin-right: 10px; /* Add margin between cards */
    width: 300px; /* Adjust card width as needed */
}

</style>