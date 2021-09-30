<template>
    <v-card tile class="pa-1 ma-1" color="grey lighten-3">
        <v-card-title color="primary">ジャンルを決定する</v-card-title>
        <v-card-text> 
            <v-row>
                <v-col v-for="item in items" :key="item.src" cols="4" align="center">
                    <v-card
                        @click="chooseGenre(item)"
                        :color="item.backgroundColor"
                        max-width="300"
                    >
                        <v-img 
                            class="imgOpacity"
                            alt="item.name"
                            contain
                            :src="item.src" />
                    </v-card>
                    <span class="text-h6 d-flex justify-center">{{item.name}}</span>
                </v-col>
            </v-row>
            <v-row> 
                <v-btn
                    dark
                    color="primary"
                    to="/main/finder" 
                >
                    <v-icon>mdi-arrow-left</v-icon>
                    戻る 
                </v-btn>  
                <!--<v-spacer />
                <v-btn
                    dark
                    color="primary"
                    @click="accessNextPage"
                >
                    次に進む    
                    <v-icon>mdi-arrow-right</v-icon>
                </v-btn>  -->
            </v-row>
        </v-card-text>

        <v-snackbar
            v-model="snackbar"
            timeout="2000"
        >ジャンルを選択してください
        </v-snackbar>
    </v-card>
</template>
<script>
export default{
    data: () => ({
        items: [
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
            for (let item of this.items){
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

