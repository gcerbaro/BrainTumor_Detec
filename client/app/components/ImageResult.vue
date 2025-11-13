<script lang="ts">
export interface ImageResultData {
  image: File;
  prob?: number;
  error?: unknown;
}
</script>

<script setup lang="ts">
const { data, tresholds = [0.05, 0.3, 0.95] } = defineProps<{
  data: ImageResultData;
  tresholds?: [number, number, number];
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

const color = computed(() => {
  if (data.prob == undefined) return "neutral";
  if (data.prob < tresholds[0]) return "success";
  if (data.prob < tresholds[1]) return "info";
  if (data.prob < tresholds[2]) return "warning";
  return "error";
});

const icon = computed(() => {
  if (data.prob == undefined) return "";
  if (data.prob < tresholds[1]) return "material-symbols-check";
  return "material-symbols-warning-outline";
});

const title = computed(() => {
  if (data.prob == undefined) return "Carregando...";
  if (data.prob < tresholds[0]) return "Nenhum tumor detectado";
  if (data.prob < tresholds[1]) return "Fracos indícios de tumor detectado";
  if (data.prob < tresholds[2]) return "Possível tumor detectado";
  return "Tumor detectado";
});

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
      <UProgress v-if="data.prob == undefined" color="neutral" />
      <UAlert
        v-else-if="data.error"
        color="error"
        icon="material-symbols-error-circle-rounded-outline-sharp"
        :title="String(data.error)"
      />
      <UAlert
        v-else
        :color="color"
        :icon="icon"
        :title="`${title} (${accuracyFormatted})`"
      />
    </template>
  </UCard>
</template>
