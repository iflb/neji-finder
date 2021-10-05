<template>
    <div>
        <v-row v-if="headerIsOn" class="py-5">
            <v-col class="text-body-1">
                {{headerTitle}}を選ぶ
            </v-col>
        </v-row>
         <carousel 
            :per-page="['md','lg','xl'].includes($vuetify.breakpoint.name) ? numItemsForDesktop : numItemsForMobile" 
            pagination-color="#42A5F5"
            :touchDrag="true"
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
    computed: {
        numItemsForMobile() {
            return this.inputItems.length ? Math.min(3, this.inputItems.length) : 3;
        },
        numItemsForDesktop() {
            return this.inputItems.length ? Math.min(5, this.inputItems.length) : 5;
        },
    },
    methods:{
        emitItem(item){
            this.$emit('update-query', item);
        }
    }
}
</script>
