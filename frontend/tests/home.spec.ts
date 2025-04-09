import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('http://localhost:5173/');
  await page.getByRole('link', { name: 'términos y condiciones', exact: true }).click();
  await page.getByRole('heading', { name: '¿Quienes Somos?' }).click();
  await page.getByRole('img', { name: 'Logo Pawtel' }).click();
  const page1Promise = page.waitForEvent('popup');
  await page.getByRole('link', { name: 'Instagram' }).click();
  const page1 = await page1Promise;
  const page2Promise = page.waitForEvent('popup');
  await page.getByRole('link', { name: 'X' }).click();
  const page2 = await page2Promise;
  const page3Promise = page.waitForEvent('popup');
  await page.getByRole('link', { name: 'TikTok' }).click();
  const page3 = await page3Promise;
  await page.getByRole('heading', { name: '¿Tienes un alojamiento?' }).click();
  await page.getByRole('link', { name: 'Logo' }).click();
  await page.getByRole('link', { name: 'Obtener 20% de descuento →' }).click();
  await page.getByRole('link', { name: 'Logo' }).click();
  await page.getByRole('button', { name: '¡Quiero unirme!' }).click();
  await page.getByRole('link', { name: 'Logo' }).click();
  await page.getByText('Sobre Nosotros Contacto Iniciar SesiónCrear Cuenta').click();
  await page.getByRole('navigation').getByRole('link', { name: 'Contacto' }).click();
  await page.getByRole('link', { name: 'Sobre Nosotros', exact: true }).click();
  await page.getByRole('link', { name: 'Logo' }).click();
});