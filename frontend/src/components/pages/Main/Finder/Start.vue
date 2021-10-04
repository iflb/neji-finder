<template>
    <v-card class="pa-1 ma-1" color="grey lighten-3">
        <v-card-title>検索を開始する</v-card-title>
        <v-card-text> 
            <v-row class="d-flex justify-center pb-2"> 
                <v-btn
                    dark
                    color="primary"
                    width="50%"
                    @click="emitComponentName"
                >
                    <v-icon>mdi-magnify</v-icon>
                    形状から検索
                </v-btn> 
            </v-row>
            <v-row class="d-flex justify-center pb-2"> 
                <v-btn
                    dark
                    width="50%"
                    color="primary"
                >
                    <v-icon>mdi-magnify</v-icon>
                    規格から検索
                </v-btn>  
            </v-row>
            <v-row class="d-flex justify-center pb-2"> 
                <v-btn
                    dark
                    width="50%"
                    color="primary"
                >
                    <v-icon>mdi-magnify</v-icon>
                    キーワードから検索
                </v-btn>  
            </v-row>
        </v-card-text>   

    </v-card>
</template>
<script>
export default {
    methods:{
        emitComponentName(){
            this.$emit( 'emit-component-name', 'query-genre' );
        }
    },
    mounted(){
        this.$emit('add-step', 1);
    }
}
</script>
