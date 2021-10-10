<template>
    <v-card tile class="pa-1 ma-1" flat color="grey lighten-3">
        <v-card-title color="primary">ジャンルを決定する</v-card-title>
        <v-card-text> 
            <card-button
                :headerIsOn="false"
                :inputItems="icons"
                @update-query="chooseGenre"
                :labelIsOn="true"
            />
            <v-divider class="pt-3"/>
            <page-transition-button 
                :nextIsNecessary="false"
                @click-back="backToPreviousPage"
            />
        </v-card-text>
    </v-card>
</template>
<script>
import CardButton from '../../CardButton'
import PageTransitionButton from '../../PageTransitionButton'
export default{
    components:{
        CardButton,
        PageTransitionButton
    },
    data: () => ({
        icons: [
            { 
                name: "おねじ", 
                src: require("@/assets/icons/1_bolt.jpg"), 
                backgroundColor: "#FFFFFF" 
            },
            { 
                name: "めねじ", 
                src: require("@/assets/icons/2_nut.jpg"), 
                backgroundColor: "#FFFFFF" 
            },
            { 
                name: "座金", 
                src: require("@/assets/icons/3_washer.jpg"), 
                backgroundColor: "#FFFFFF" 
            },
        ],
        chosenGenre: '',
    }),
    props:["duct"],
    methods: {
        chooseGenre(clickedGenre){
            this.chosenGenre = clickedGenre.name;
            this.$emit( 'emit-genre', this.chosenGenre );
            if(["めねじ","座金"].includes(this.chosenGenre)){
                this.$emit( 'emit-component-name', 'query-nut-washer-shape' );
            }else{
                this.$emit( 'emit-component-name', 'query-bolt-shape' );
            }
        },
        backToPreviousPage(){
            this.$emit( 'emit-component-name', 'start-screen' );
        }
    }, 
    mounted(){
        this.$emit('add-step',1)
    }
}
</script>
<style>
.imgOpacity{
    opacity: 0.75
}
</style>

