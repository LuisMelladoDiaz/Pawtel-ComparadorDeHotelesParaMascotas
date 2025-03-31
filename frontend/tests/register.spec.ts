import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('http://localhost:5173/');
  await page.getByRole('link', { name: 'Crear Cuenta', exact: true }).click();
  await page.getByRole('textbox', { name: 'Nombre de Usuario' }).click();
  await page.getByRole('textbox', { name: 'Nombre de Usuario' }).fill('dfloress');
  await page.getByRole('textbox', { name: 'Correo Electrónico' }).click();
  await page.getByRole('textbox', { name: 'Correo Electrónico' }).fill('dfloress@gmail.com');
  await page.getByRole('textbox', { name: 'Teléfono' }).click();
  await page.getByRole('textbox', { name: 'Teléfono' }).fill('+34666554433');
  await page.getByLabel('¿Qué eres?').selectOption('customer');
  await page.getByPlaceholder('Crea una contraseña segura').fill('password123');
  await page.getByRole('textbox', { name: 'Confirmar contraseña' }).click();
  await page.getByRole('textbox', { name: 'Confirmar contraseña' }).fill('password123');
  const page1Promise = page.waitForEvent('popup');
  await page.locator('form div').filter({ hasText: 'Acepto los términos y' }).click();
  const page1 = await page1Promise;
  await page1.goto('http://localhost:5173/terminos-y-condiciones');
  await page.getByRole('checkbox', { name: 'Acepto los términos y' }).check();
  await page.getByRole('button', { name: 'Registrarse' }).click();
});