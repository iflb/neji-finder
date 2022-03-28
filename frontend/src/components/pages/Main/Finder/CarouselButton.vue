<template>
    <v-card color="transparent" flat>
        <v-row v-if="headerIsOn" class="pt-3 mb-4">
            <v-col>
                <v-card dark flat color="#424242">
                    <span class="text-subtitle-1 d-flex justify-center">{{headerTitle}}</span>
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
                v-for="(item, itemIdx) in inputItems" 
                :key="itemIdx" 
                align="center"
            >
                <v-card
                    class="d-flex align-center justify-center"
                    @click="emitItem(item)"
                    :color="itemBackgroundColors[item.name]"
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
    model: {
        prop: 'selectedItemName',
        event: 'update',
    },
    components:{
        Carousel,
        Slide
    },

    props: {
        selectedItemName: { type: String },
        headerTitle: { type: String },
        inputItems: { type: Array },
    },

    computed: {
        headerIsOn() {
            return (this.headerTitle !== undefined);
        },
        numItemsForMobile() {
            return this.inputItems.length ? Math.min(3, this.inputItems.length) : 3;
        },
        numItemsForDesktop() {
            return this.inputItems.length ? Math.min(3, this.inputItems.length) : 3;
        },
        itemBackgroundColors() {
            let itemBackgroundColors = {};
            for (let item of this.inputItems) {
                let itemName = item.name;
                if (itemName === this.selectedItemName) {
                    itemBackgroundColors[itemName] = '#FFCA28';
                } else {
                    itemBackgroundColors[itemName] = '#FFFFFF';
                }
            }
            return itemBackgroundColors;
        },
    },
    methods:{
        emitItem(item){
            if (this.selectedItemName === item.name) {
                this.$emit('update', null);
            } else {
                this.$emit('update', item.name);
            }
        }
    }
}
</script>
