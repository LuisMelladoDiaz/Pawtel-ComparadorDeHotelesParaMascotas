import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('http://localhost:5173/');
  await page.locator('div').filter({ hasText: /^Selecciona una ciudadTodasAlmeríaCádizCórdobaGranadaHuelvaJaénMálagaSevilla$/ }).getByRole('combobox').selectOption('Córdoba');
  await page.locator('div').filter({ hasText: /^Elige un tipo de mascotaCualquieraPájaroGatoPerroMixto$/ }).getByRole('combobox').selectOption('');
  await page.getByRole('button', { name: 'Buscar' }).click();
  await page.getByRole('spinbutton').first().click();
  await page.getByRole('spinbutton').first().fill('30');
  await page.getByText('Filtrar por:Precio por Noche€-€Ordenar por...NombrePrecio MáximoPrecio Mí').click();
  await page.locator('div').filter({ hasText: /^Ordenar por\.\.\.NombrePrecio MáximoPrecio Mínimo$/ }).getByRole('combobox').selectOption('max_price_filters');
  await page.locator('div').filter({ hasText: /^Ordenar por\.\.\.NombrePrecio MáximoPrecio Mínimo$/ }).getByRole('combobox').selectOption('min_price_filters');
  await page.getByRole('button', { name: 'ASC ' }).click();
  await page.getByRole('button', { name: 'DESC ' }).click();
  await page.locator('.info-container').first().click();
  await page.locator('a > .px-4').first().click();
});