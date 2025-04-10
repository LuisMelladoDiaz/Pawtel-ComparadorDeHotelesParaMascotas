import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('http://localhost:5173/login');
  await page.getByRole('textbox', { name: 'Nombre de Usuario' }).click();
  await page.getByRole('textbox', { name: 'Nombre de Usuario' }).fill('customer1');
  await page.getByRole('textbox', { name: 'Contraseña' }).click();
  await page.getByRole('textbox', { name: 'Contraseña' }).fill('password123');
  await page.getByRole('button', { name: 'Iniciar Sesión' }).click();
  await page.getByRole('button', { name: 'Buscar' }).click();
  await page.locator('a > .px-4').first().click();
  await page.getByRole('button', { name: 'Reservar' }).first().click();
  await page.getByRole('button', { name: 'Cancelar' }).click();
  await page.getByRole('button', { name: 'Reservar' }).first().click();
  await page.getByRole('row', { name: 'Fechas:  Establece un rango' }).locator('i').click();
  await page.getByRole('textbox', { name: 'Selecciona un rango de fechas' }).click();
  await page.locator('div:nth-child(28) > .flatpickr-innerContainer > .flatpickr-rContainer > .flatpickr-days > .dayContainer > span:nth-child(25)').click();
  await page.locator('div').filter({ hasText: 'AprilMayJuneJulyAugustSeptemberOctober MonTueWedThuFriSatSun' }).getByLabel('April 25,').click();
  await page.getByRole('button', { name: 'Ir al Pago' }).click();
});