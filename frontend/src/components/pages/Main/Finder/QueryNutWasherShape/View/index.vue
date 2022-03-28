<template>
    <v-card class="pa-1 ma-1" color="grey lighten-3">
        <v-card-title>{{genre}}の形状を選ぶ</v-card-title>
        <v-card-text> 
            <card-button
                v-model="selectedShapeName"
                :input-items="selectableShapeIcons"
                :label-is-on="true"
            />
            <v-divider class="pt-3"/>
            <page-transition-button 
                :next-is-necessary="false"
                @click-back="unsetGenre"
            />
        </v-card-text>   
    </v-card>
</template>
<script>
import { Duct } from '@iflb/ducts-client'
import { nut_washer_icons } from '../../shape_profile.js'
import CardButton from '../../CardButton' 
import PageTransitionButton from '../../PageTransitionButton'
export default{
    watch: {
        selectedShapeName() {
            this.send_query();
        },
    },
    components:{
        CardButton,
        PageTransitionButton
    },
    data: () => ({
        syncStateReceiveRequestId:null,
        selectedShapeName: null,
    }),

    props: {
        duct: { type: Duct },
        syncId: { type: String },
        genre: { type: String },
    },

    computed:{
        selectableShapeIcons(){
            return nut_washer_icons[this.genreEng]
        },
        query() {
            let query = {};
            if (this.selectedShapeName !== null) {
                query[this.queryKey] = this.selectedShapeName;
            }
            return query;
        },
        queryKey() {
            switch (this.genreEng) {
                case 'nut':
                    return 'ナット形状';
                case 'washer':
                    return '座金形状';
                default:
                    return null;
            }
        },
        genreEng() {
            switch (this.genre) {
                case 'めねじ':
                    return 'nut';
                case '座金':
                    return 'washer';
                default:
                    return null;
            }
        },
    },
    methods: {
        send_query() {
            if (this.syncId === null) return;
            this.duct.send(
                this.duct.nextRid(), 
                this.duct.EVENT.SYNC_STATE_UPDATE,
                {'sync_id': this.syncId, 'genre': this.genre, 'query': this.query},
            );
        },
        unsetGenre(){
            this.duct.send(
                this.duct.nextRid(), 
                this.duct.EVENT.SYNC_STATE_UPDATE,
                {
                    sync_id: this.syncId,
                },
            );
        },
        accessNextPage(){
            this.$emit( 'emit-query', this.query );
            this.$emit( 'emit-component-name', 'query-spec' );
        },
        backToPreviousPage(){
            this.$emit( 'emit-component-name', 'query-genre' );
        }
    }, 
    created(){
        this.syncStateReceiveRequestId = this.duct.nextRid();
        this.$emit(
            'register-sync-state-receive-handler',
            {
                rid: this.syncStateReceiveRequestId,
                handler: (rid, eid, data) => {
                    if(!Object.keys(data).includes('genre')){
                        this.backToPreviousPage();
                    }else{
                        if(Object.keys(data.query).includes(this.queryKey)){
                            this.selectedShapeName = data.query[this.queryKey];
                        }

                        if(Object.keys(data).includes('spec')){
                            this.accessNextPage();
                        }else{
                            this.$nextTick(() => {
                                this.$vuetify.goTo(document.body.scrollHeight);
                            });
                        }
                    }
                },
            }
        );
    },
    mounted(){
        this.$emit('add-step', 2);
    },
    destroyed(){
        this.$emit(
            'unregister-sync-state-receive-handler',
            { rid: this.syncStateReceiveRequestId },
        );
    },
}
</script>
