<template>
    <v-card color="transparent" flat>
        <v-row v-if="headerIsOn" class="pt-3 mb-4">
            <v-col>
                <v-card dark flat color="#424242">
                    <span class="text-subtitle-1 d-flex justify-center">{{headerTitle}}を選ぶ</span>
                </v-card>
            </v-col>
        </v-row>
        <carousel 
            :per-page="['md','lg','xl'].includes($vuetify.breakpoint.name) ? numItemsForDesktop : numItemsForMobile" 
            pagination-color="#E53935"
            pagination-active-color="#3949AB"
            :touchDrag="true"
        >
            <slide 
                v-for="item in inputItems" 
                :key="item.name" 
                align="center"
            >
                <v-card
                    class="d-flex align-center justify-center"
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
    </v-card>
</template>
<script>
import { Carousel, Slide } from 'vue-carousel'
export default{
    components:{
        Carousel,
        Slide
    },
    props:["headerIsOn","headerTitle","inputItems"],
    computed: {
        numItemsForMobile() {
            return this.inputItems.length ? Math.min(3, this.inputItems.length) : 3;
        },
        numItemsForDesktop() {
            return this.inputItems.length ? Math.min(3, this.inputItems.length) : 3;
        },
    },
    methods:{
        emitItem(item){
            this.$emit('update-query', item);
        }
    }
}
</script>
