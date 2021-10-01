<template>
    <v-card tile class="pa-1 ma-1" color="grey lighten-3">
        <v-card-title color="primary">ジャンルを決定する</v-card-title>
        <v-card-text> 
            <card-button
                :headerIsOn="false"
                :inputItems="icons"
                @update-query="chooseGenre"
                :labelIsOn="true"
            />
            <v-divider />
            <v-row class="pt-5"> 
                <v-btn
                    dark
                    color="primary"
                    to="/main/finder" 
                >
                    <v-icon>mdi-arrow-left</v-icon>
                    戻る 
                </v-btn>  
            </v-row>
        </v-card-text>
    </v-card>
</template>
<script>
import CardButton from '../../CardButton'
export default{
    components:{
        CardButton
    },
    data: () => ({
        icons: [
            { name: "おねじ", src: require("@/assets/icons/1_bolt.jpg"), backgroundColor: "#FFFFFF" },
            { name: "めねじ", src: require("@/assets/icons/2_nut.jpg"), backgroundColor: "#FFFFFF" },
            { name: "座金", src: require("@/assets/icons/3_washer.jpg"), backgroundColor: "#FFFFFF" },
        ],
        chosenGenre: '',
        path:'',
        snackbar:false,
    }),
    props:["duct"],
    methods: {
        chooseGenre(clickedGenre){
            this.chosenGenre = clickedGenre.name;
            clickedGenre.backgroundColor = "#FFB300";
            for (let item of this.icons){
                if(item.name !== clickedGenre.name){
                    item.backgroundColor = "#FFFFFF";
                }
            }
            if(["めねじ","座金"].includes(this.chosenGenre)){
                this.path = "QueryNutWasherShape"
            }else{
                this.path = "QueryBoltShape"
            }
            this.accessNextPage();
        },
        accessNextPage(){
            if (this.path != ''){
                this.$router.push({
                    name: this.path,
                    params: {"genre":this.chosenGenre}
                });
            }else{
                this.snackbar = true;
            }
        },
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

