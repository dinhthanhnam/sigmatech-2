# Next application
## Features
* UI: Shadcn ui, TailwindCSS v4, bunch of customized components.
* State management: Mostly contextAPI, zustand sometimes, redux (could be never), redux with persistence (could be).
* Mostly server side render (if possible)

## Subjectiveness
* Common/Global components go to ./components/app/common (Naming convention is Pascal Case)
* While Customized/Local components stay inside page.tsx or other files in the same dir (This file is named in Kebab Case)
* Context, context provider and hooks stay inside context.tsx (Same level as page.tsx)
* Global hooks like use-mobile.tsx (Kebab Case) go to ./hooks
* Utilities go to ./utils (Naming convention is Kebab Case)
* Constants go to ./constant or ./utils/constant
* Type go to ./types (Naming convention is Pascal Case)
* Services/Api instance go to ./lib ./lib/services
* Service is named in Kebab Case
* Logic server side/ client side also go to ./lib