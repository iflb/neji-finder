<template>
    <v-card class="pa-1 mx-1 my-4" color="grey lighten-3">
        <v-card-title>最近閲覧した商品</v-card-title>
        <v-card-text> 
                <carousel-button
                   :input-items="itemHistory"
                   @update-query="accessResultPage"
                />
        </v-card-text>   

    </v-card>
</template>
<script>
import CarouselButton from '../../CarouselButton'
export default {
    components:{
        CarouselButton
    },
    data: () => ({
        itemHistory:[],
        srcPaths:[],
    }),
    methods:{
        accessResultPage(item){
            this.$emit( 'emit-item', [item.data] );
            this.$emit( 'emit-component-name', 'result' );
            this.$nextTick(() => {
                this.$vuetify.goTo(0);
            });
        },
        emitComponentName(){
            this.$emit( 'emit-component-name', 'query-genre' );
        }
    },
    created(){
        const collections = Object.keys(window.localStorage).filter(key => key.includes('neji-product')).map((key) => window.localStorage[key]);
        collections.forEach((item) => 
            this.itemHistory.push(JSON.parse(item))
        );
    }
}
</script>
