<template>
    <v-card class="pa-1 ma-1" color="grey lighten-3">
        <v-card-title>ねじを探す</v-card-title>
        <v-card-text> 
            <v-row class="d-flex justify-center pb-2"> 
                <v-btn
                    dark
                    color="primary"
                    to="/main/finder/query-genre" 
                >
                    <v-icon>mdi-magnify</v-icon>
                    検索を開始する    
                </v-btn>  
            </v-row>
        </v-card-text>   
    </v-card>
</template>
<script>
export default {
    mounted(){
        this.$emit('add-step', 1);
    }
}
</script>
