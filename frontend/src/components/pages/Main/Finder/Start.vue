<template>
    <v-card class="pa-1 ma-1" color="grey lighten-3">
        <v-card-title>検索を開始する</v-card-title>
        <v-card-text> 
            <v-row class="d-flex justify-center pb-2" style="font-size:1.2em"> 
                <v-col cols="10" md="8">
                    <v-btn
                        dark
                        color="primary"
                        width="100%"
                        height="100px"
                        @click="emitComponentName"
                    >
                        <v-icon>mdi-magnify</v-icon>
                        形状から検索
                    </v-btn> 
                </v-col>
                <v-col cols="10" md="8">
                    <v-btn
                        color="primary"
                        width="100%"
                        height="100px"
                        disabled
                    >
                        <v-icon>mdi-magnify</v-icon>
                        規格から検索
                    </v-btn>  
                </v-col>
                <v-col cols="10" md="8">
                    <v-btn
                        color="primary"
                        width="100%"
                        height="100px"
                        disabled
                    >
                        <v-icon>mdi-magnify</v-icon>
                        キーワードから検索
                    </v-btn>  
                </v-col>
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
