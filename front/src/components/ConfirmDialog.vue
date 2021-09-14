<template>
  <v-dialog v-model="dialog" max-width="600">
    <v-card>
      <v-card-title class="text-h5"> Решение о продаже</v-card-title>

      <v-card-text>
        Вы хотите продать портфель? Если Вы выберете "продать", период
        закончится.
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>

        <v-btn color="green darken-1" @click="continueKeeping">
          Оставить
        </v-btn>

        <v-btn color="red darken-1" @click="sell"> Продать</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  props: ["dialog"],
  data: () => ({}),
  methods: {
    sell() {
      this.$emit("sell");
    },
     sell() {
      this.$emit("continueKeeping");
    },
  },
};
</script>
