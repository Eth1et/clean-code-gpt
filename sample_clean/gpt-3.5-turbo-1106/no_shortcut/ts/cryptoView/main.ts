import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { AppModule } from './app/app.module';

const bootstrapAppModule = () => {
  platformBrowserDynamic()
    .bootstrapModule(AppModule)
    .catch(error => console.error(error));
};

bootstrapAppModule();