<template>
  <UApp>
    <UHeader :toggle="false" class="z-100!">
      <template #left>
        <NuxtLink to="/">
          <h1 class="font-extrabold text-xl flex items-center gap-4">
            <UIcon name="iconoir-brain-research" size="1.5em" />
            <span class="max-sm:sr-only">Detector de Tumores Cerebrais</span>
          </h1>
        </NuxtLink>
      </template>

      <template #right>
        <UColorModeButton />

        <UButton
          to="https://github.com/gcerbaro/BrainTumor_Detec"
          target="_blank"
          icon="i-simple-icons-github"
          aria-label="GitHub"
          color="neutral"
          variant="ghost"
        />
      </template>
    </UHeader>

    <UMain class="flex flex-col">
      <NuxtPage />
    </UMain>

    <USeparator icon="i-simple-icons-nuxtdotjs" />

    <UFooter>
      <template #left>
        <p class="text-sm text-muted">
          Built with Nuxt UI • © {{ new Date().getFullYear() }}
        </p>
      </template>

      <template #right>
        <UButton
          to="https://github.com/gcerbaro/BrainTumor_Detec"
          target="_blank"
          icon="i-simple-icons-github"
          aria-label="GitHub"
          color="neutral"
          variant="ghost"
        />
      </template>
    </UFooter>
  </UApp>
</template>
