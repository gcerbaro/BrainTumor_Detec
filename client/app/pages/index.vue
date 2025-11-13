<script setup lang="ts">
import type { FormSubmitEvent } from "@nuxt/ui";
import type { schema } from "@/components/UploadForm.vue";
import type { ImageResultData } from "~/components/ImageResult.vue";

type PredictResults = {
  filename: string;
  prob: number;
}[];

const { public: config } = useRuntimeConfig();

const viewport = useViewport();
const state = reactive<Partial<schema>>({
  images: [],
});

const submission = reactive({
  results: [] as ImageResultData[],
});

const onSubmit = async (event: FormSubmitEvent<schema>) => {
  const {
    data: { images },
  } = event;

  const results: ImageResultData[] = images.map((img) =>
    reactive({ image: img })
  );

  submission.results.unshift(...results);
  state.images = [];

  const endpoint = `${config.apiBaseURL}/predict`;
  const formData = new FormData();

  images.forEach((img) => formData.append("files", img));

  try {
    const rawResults: PredictResults = await fetch(endpoint, {
      method: "POST",
      body: formData,
    }).then((res) => res.json());

    const resultMap = Object.fromEntries(
      rawResults.map((result) => [result.filename, result])
    );

    results.forEach((result) => {
      if (resultMap[result.image.name]) {
        result.prob = resultMap[result.image.name]!.prob;
      } else {
        result.error = new Error("Resultado não encontrado");
      }
    });
  } catch (error) {
    console.error(error);
    results.forEach((res) => {
      res.error = new Error(`Não foi possível processar as imagens: ${error}`);
    });
  }
};

const tresholds = reactive<[number, number, number]>([0.05, 0.3, 0.95]);
</script>

<template>
  <div class="w-full lg:flex-1 flex flex-col lg:flex-row items-stretch">
    <div class="flex-1 flex flex-col">
      <UHeader
        title="Submissão de Imagens"
        class="top-(--ui-header-height)"
        :toggle="false"
      >
        <template #right>
          <UButton
            type="submit"
            label="Enviar"
            color="primary"
            variant="subtle"
            size="lg"
            trailing-icon="material-symbols-settings-b-roll-outline-rounded"
            class="cursor-pointer"
            :disabled="!state.images?.length"
            form="upload-form"
          />
        </template>
      </UHeader>

      <div class="flex-1 flex flex-col items-center justify-center p-2 lg:p-4">
        <UploadForm
          id="upload-form"
          v-model:state="state"
          :on-submit="onSubmit"
        />
      </div>
    </div>

    <USeparator
      v-if="viewport.isGreaterOrEquals('lg')"
      orientation="vertical"
      class="h-[--webkit-fill-available]"
    />
    <USeparator v-else />

    <div class="flex-1 flex flex-col">
      <UHeader
        title="Resultados"
        class="top-(--ui-header-height)"
        :toggle="false"
      >
        <template #right>
          <UPopover>
            <UButton
              color="neutral"
              variant="ghost"
              icon="icon-park-outline-config"
              class="cursor-pointer"
            />

            <template #content>
              <div class="p-4 space-y-8">
                <UFormField
                  v-for="(treshold, i) in tresholds"
                  :key="i"
                  name="treshold"
                  :label="`Limite ${i + 1} (${(treshold * 100).toFixed(0)}%)`"
                >
                  <USlider
                    v-model="tresholds[i]"
                    class="w-64"
                    :min="0.01"
                    :max="1"
                    :step="0.01"
                    :tooltip="{
                      text: `${(treshold * 100).toFixed(0)}%`,
                    }"
                  />
                </UFormField>
              </div>
            </template>
          </UPopover>

          <UButton
            type="button"
            label="Limpar resultados"
            color="neutral"
            variant="subtle"
            size="lg"
            trailing-icon="material-symbols-clear-all"
            class="cursor-pointer"
            :disabled="!submission.results.length"
            @click="submission.results = []"
          />
        </template>
      </UHeader>

      <div class="flex-1 flex flex-col gap-8 p-2 lg:p-4">
        <div
          v-if="!submission.results.length"
          class="text-center flex-1 space-y-8 py-10"
        >
          <UIcon name="streamline-cards" size="4em" class="text-dimmed" />
          <h3 class="text-lg text-dimmed">Nenhuma imagem submetida ainda</h3>
        </div>
        <template v-else>
          <ImageResult
            v-for="data in submission.results"
            :key="data.image.name"
            :tresholds="tresholds"
            :data="data"
          />
        </template>
      </div>
    </div>
  </div>
</template>
