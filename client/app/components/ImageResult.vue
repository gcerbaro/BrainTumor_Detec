<script lang="ts">
export interface ImageResultData {
  image: File;
  prob?: number;
  error?: unknown;
}
</script>

<script setup lang="ts">
const { data, treshold = 0.5 } = defineProps<{
  data: ImageResultData;
  treshold?: number;
}>();

const src = computed(() => URL.createObjectURL(data.image));

const revoke = (url: string) => {
  URL.revokeObjectURL(url);
};

watch(src, (_, oldSrc) => {
  revoke(oldSrc);
});

onBeforeUnmount(() => {
  revoke(src.value);
});

const isDetected = computed(
  () => data.prob != undefined && data.prob >= treshold
);

const accuracyFormatted = computed(() =>
  data.prob === undefined ? "Carregando..." : `${(data.prob * 100).toFixed(2)}%`
);
</script>

<template>
  <UCard variant="subtle" class="w-full">
    <template #header>
      <p>{{ data.image.name }}</p>
    </template>

    <div class="w-full flex items-center justify-center">
      <img
        :src="src"
        :alt="data.image.name"
        class="rounded-lg"
        @load="() => revoke(src)"
      />
    </div>

    <template #footer>
      <UProgress v-if="data == undefined" color="neutral" />
      <UAlert
        v-else-if="isDetected"
        color="warning"
        icon="material-symbols-warning"
        :title="`Possível tumor detectado (${accuracyFormatted})`"
      />
      <UAlert
        v-else-if="!data.error"
        color="success"
        icon="material-symbols-check"
        :title="`Tumor não detectado (${accuracyFormatted})`"
      />
      <UAlert
        v-else
        color="error"
        icon="material-symbols-error-circle-rounded-outline-sharp"
        :title="String(data.error)"
      />
    </template>
  </UCard>
</template>
