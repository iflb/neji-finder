<template>
    <v-card color="transparent" flat>
        <v-row v-if="headerIsOn" class="pt-3">
            <v-col>
                <v-card dark flat color="#424242">
                    <span class="text-subtitle-1 d-flex justify-center">{{headerTitle}}を選ぶ</span>
                </v-card>
            </v-col>
        </v-row>
        <v-row justify="center">
            <v-col 
                v-for="item in inputItems" 
                :key="item.jan" 
                cols="4" 
                align="center"
            >
                <v-card
                    @click="emitItem(item)"
                    :color="item.backgroundColor"
                    max-width="100"
                    hover
                >
                    <v-img 
                        class="imgOpacity"
                        contain
                        :src="item.src" />
                </v-card>
                <span v-if="labelIsOn" class="text-h8 d-flex justify-center">{{item.name}}</span>
            </v-col>
        </v-row>
    </v-card>
</template>
<script>
export default{
    props:["headerIsOn","headerTitle","inputItems","labelIsOn"],
    methods:{
        emitItem(item){
            this.$emit('update-query', item);
        }
    }
}
</script>
<style>
.imgOpacity{
    opacity: 0.75
}
</style>
