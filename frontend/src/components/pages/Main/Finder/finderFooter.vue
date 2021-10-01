<template>
    <v-row class="pt-7"> 
        <v-btn
            dark
            color="primary"
            to="previousPagePath" 
        >
            <v-icon>mdi-arrow-left</v-icon>
            戻る    
        </v-btn>  
        <v-spacer />
        <v-btn
            dark
            color="primary"
            @click="accessNextPage"
        >
            次に進む 
            <v-icon>mdi-arrow-right</v-icon>
        </v-btn>  
    </v-row>
</template>
<script>
export default{
    props:["previousPagePath","nextPagePath"]
}
</script>
