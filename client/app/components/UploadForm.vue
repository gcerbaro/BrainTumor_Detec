<script lang="ts">
import * as z from "zod";
import type { FormSubmitEvent } from "@nuxt/ui";

const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
const MIN_DIMENSIONS = { width: 200, height: 200 };
const MAX_DIMENSIONS = { width: 4096, height: 4096 };
const ACCEPTED_IMAGE_TYPES = [
  "image/jpeg",
  "image/jpg",
  "image/png",
  "image/webp",
];

const formatBytes = (bytes: number, decimals = 2) => {
  if (bytes === 0) return "0 Bytes";
  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return (
    Number.parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + " " + sizes[i]
  );
};

export const schema = z.object({
  images: z
    .instanceof(File, {
      message: "Por favor, selecione uma imagem.",
    })
    .refine((file) => file.size <= MAX_FILE_SIZE, {
      message: `A imagem é muito grande. Por favor, selecione uma imagem menor que ${formatBytes(
        MAX_FILE_SIZE
      )}.`,
    })
    .refine((file) => ACCEPTED_IMAGE_TYPES.includes(file.type), {
      message:
        "Por favor, selecione um tipo de imagem válido (JPEG, PNG, ou WebP).",
    })
    .refine(
      (file) =>
        new Promise((resolve) => {
          const reader = new FileReader();
          reader.onload = (e) => {
            const img = new Image();
            img.onload = () => {
              const meetsDimensions =
                img.width >= MIN_DIMENSIONS.width &&
                img.height >= MIN_DIMENSIONS.height &&
                img.width <= MAX_DIMENSIONS.width &&
                img.height <= MAX_DIMENSIONS.height;
              resolve(meetsDimensions);
            };
            img.src = e.target?.result as string;
          };
          reader.readAsDataURL(file);
        }),
      {
        message: `As dimensões da imagem são inválidas. Por favor, selecione uma imagem entre ${MIN_DIMENSIONS.width}x${MIN_DIMENSIONS.height} e ${MAX_DIMENSIONS.width}x${MAX_DIMENSIONS.height} pixels.`,
      }
    )
    .array()
    .max(5, "Por favor, envie no máximo 5 imagens por vez."),
});

export type schema = z.output<typeof schema>;
</script>

<script setup lang="ts">
const { onSubmit } = defineProps<{
  onSubmit: (event: FormSubmitEvent<schema>) => void | Promise<void>;
}>();

const state = defineModel<Partial<schema>>("state", { required: true });
</script>

<template>
  <UForm
    :schema="schema"
    :state="state"
    class="space-y-4 w-full h-full"
    @submit="onSubmit"
  >
    <UFormField name="images">
      <UFileUpload
        v-model="state.images"
        :accept="ACCEPTED_IMAGE_TYPES.join(',')"
        class="min-h-48 cursor-pointer"
        layout="grid"
        multiple
        label="Adicione suas imagens aqui (max. 5 por vez)"
        :description="`JPG, PNG, ou WebP (max. ${formatBytes(MAX_FILE_SIZE)})`"
      />
    </UFormField>
  </UForm>
</template>
