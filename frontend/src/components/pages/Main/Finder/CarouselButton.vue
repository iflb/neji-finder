<template>
    <div>
        <v-row v-if="headerIsOn" class="py-5">
            <v-col class="text-body-1">
                {{headerTitle}}を選ぶ
            </v-col>
        </v-row>
         <carousel 
            :per-page="3" 
            :mouse-drag="false" 
            pagination-color="#42A5F5"
        >
            <slide 
                v-for="item in inputItems" 
                :key="item.src" 
                align="center"
            >
                <v-card
                    @click="emitItem(item)"
                    :color="item.backgroundColor"
                    max-width="100"
                    min-height="100"
                >
                    <v-img 
                        class="imgOpacity"
                        alt="item.name"
                        contain
                        :src="item.src" />
                </v-card>
                <span class="text-h8 d-flex justify-center">{{item.name}}</span>
            </slide>
        </carousel>
    </div>
</template>
<script>
import { Carousel, Slide } from 'vue-carousel'
export default{
    components:{
        Carousel,
        Slide
    },
    props:["headerIsOn","headerTitle","inputItems"],
    methods:{
        emitItem(item){
            this.$emit('update-query', item);
        }
    }
}
</script>
