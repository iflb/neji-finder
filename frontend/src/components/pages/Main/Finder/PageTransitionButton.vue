<template>
    <v-row> 
        <v-col>
            <v-btn
                dark
                color="indigo darken-1"
                @click="clickBackCallback"
            >
                <v-icon>mdi-arrow-left</v-icon>
                戻る    
            </v-btn>  
        </v-col>
        <v-col class="d-flex mr-auto" v-if="nextIsNecessary">
            <v-spacer />
            <v-btn
                :dark="!nextDisabled"
                :disabled="nextDisabled"
                color="indigo darken-1"
                @click="clickNextCallback"
            >
                次に進む 
                <v-icon>mdi-arrow-right</v-icon>
            </v-btn>
        </v-col> 
    </v-row>
</template>
<script>
const emptyCallback = () => {};

export default{
    props: {
        nextDisabled: { type: Boolean },
        clickBackCallback: { type: Function, default: emptyCallback },
        clickNextCallback: { type: Function, default: emptyCallback },
    },

    computed: {
        nextIsNecessary() {
            return (this.clickNextCallback !== emptyCallback);
        },
    },
}
</script>
