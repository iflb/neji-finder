<template>
    <div>
        <search-window 
            @emit-component-name ='emitComponentName'
            @emit-footer-component-name='emitFooterComponentName'
            @emit-item='emitItem'
        />
        <v-divider />
        <history-window 
            @emit-component-name ='emitComponentName'
            @emit-item='emitItem'
        /> 
    </div> 
</template>

<script>
import SearchWindow from './SearchWindow'
import HistoryWindow from './HistoryWindow'

export default {
    components: {
        SearchWindow,
        HistoryWindow,
    },

    methods: {
        emitComponentName(componentName) {
            this.$emit('emit-component-name', componentName);
        },

        emitFooterComponentName(componentName) {
            this.$emit('emit-footer-component-name', componentName);
        },

        emitItem(item) {
            this.$emit('emit-item', item);
        }
    },

    mounted() {
        this.$emit('add-step', 1);
    },
}
</script>
