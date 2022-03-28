<template>
    <v-row> 
        <v-col>
            <v-btn
                dark
                color="indigo darken-1"
                @click="$emit('click-back')"
            >
                <v-icon>mdi-arrow-left</v-icon>
                戻る    
            </v-btn>  
        </v-col>
        <v-col class="d-flex mr-auto" v-if="nextIsNecessary">
            <v-spacer />
            <v-btn
                :dark="!buttonDisabled"
                :disabled="buttonDisabled"
                color="indigo darken-1"
                @click="$emit('click-next')"
            >
                次に進む 
                <v-icon>mdi-arrow-right</v-icon>
            </v-btn>
        </v-col> 
    </v-row>
</template>
<script>
export default{
    props: {
        nextIsNecessary: { type: Boolean },
        buttonDisabled: { type: Boolean },
    },
}
</script>
