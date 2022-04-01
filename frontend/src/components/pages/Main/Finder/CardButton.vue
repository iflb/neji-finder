<template>
    <v-card color="transparent" flat>
        <v-row v-if="headerIsOn" class="pt-3">
            <v-col>
                <v-card dark flat color="#424242">
                    <span class="text-subtitle-1 d-flex justify-center">{{headerTitle}}</span>
                </v-card>
            </v-col>
        </v-row>
        <v-row justify="center">
            <v-col 
                v-for="(item, itemIdx) in inputItems" 
                :key="itemIdx" 
                cols="4" 
                align="center"
            >
                <v-card
                    @click="emitItem(item)"
                    :color="itemBackgroundColors[item.name]"
                    max-width="100"
                    hover
                >
                    <v-img 
                        class="img-opacity"
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
    model: {
        prop: 'selectedItemName',
        event: 'update',
    },

    props: {
        selectedItemName: { type: String },
        headerTitle: { type: String },
        inputItems: { type: Array },
        labelIsOn: { type: Boolean },
    },

    computed: {
        headerIsOn() {
            return (this.headerTitle !== undefined);
        },

        numInputItems() {
            return this.inputItems.length;
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

    methods: {
        emitItem(item) {
            if (this.selectedItemName === item.name) {
                this.$emit('update', null);
            } else {
                this.$emit('update', item.name);
            }
            this.$emit('input', item);
        }
    },
}
</script>

<style>
.img-opacity{
    opacity: 0.75;
}
</style>
