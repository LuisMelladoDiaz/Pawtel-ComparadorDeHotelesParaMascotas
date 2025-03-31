import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('http://localhost:5173/');
  await page.getByRole('link', { name: 'Iniciar Sesión' }).click();
  await page.getByRole('textbox', { name: 'Nombre de Usuario' }).click();
  await page.getByRole('textbox', { name: 'Nombre de Usuario' }).fill('customer1');
  await page.getByRole('textbox', { name: 'Contraseña' }).click();
  await page.getByRole('textbox', { name: 'Contraseña' }).fill('password123');
  await page.getByRole('button', { name: 'Iniciar Sesión' }).click();
});