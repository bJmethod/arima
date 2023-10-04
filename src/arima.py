import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.stattools import adfuller, kpss
import numpy as np
import scipy.stats as stats

## TODO volver esto un metodo que genere las funciones de autocorrealacion simple y parcial
## recibe una serie o un pandas dataframe
def get_auto_correlation_function():
    plot_acf(Xt, lags=5)
    plt.title('Función de Autocorrelación Simple (ACF)')
    plt.xlabel('Lag')
    plt.ylabel('ACF')
    plt.show()
    # Calcular la PACF y graficarla
    plot_pacf(Xt, lags=5)
    plt.title('Función de Autocorrelación Parcial (PACF)')
    plt.xlabel('Lag')
    plt.ylabel('PACF')
    plt.show()


def arima_model():
    modelo = sm.tsa.ARIMA(Xt, order=(1, 0, 1))
    resultado = modelo.fit()
    residuos = resultado.resid
    return {"modelo": modelo, "residuos":residuos}

## TO-DO organizar cada test en un metodo

# Prueba de Dickey-Fuller Aumentada (ADF) para estacionaridad
adf_test = adfuller(residuos)
adf_statistic, adf_pvalue, _, _, adf_critical_values, _ = adf_test
print(f'Estadística ADF: {adf_statistic}')
print(f'Valor p ADF: {adf_pvalue}')
print('Valores críticos ADF:')
for key, value in adf_critical_values.items():
    print(f'{key}: {value}')

if adf_pvalue < 0.05:
    print('Los residuos son estacionarios según la prueba ADF')
else:
    print('Los residuos no son estacionarios según la prueba ADF')

# Prueba KPSS para estacionaridad
kpss_test = kpss(residuos)
kpss_statistic, kpss_pvalue, _, kpss_critical_values = kpss_test
print(f'Estadística KPSS: {kpss_statistic}')
print(f'Valor p KPSS: {kpss_pvalue}')
print('Valores críticos KPSS:')
for key, value in kpss_critical_values.items():
    print(f'{key}: {value}')

if kpss_pvalue > 0.05:
    print('Los residuos son estacionarios según la prueba KPSS')
else:
    print('Los residuos no son estacionarios según la prueba KPSS')

# Gráfico de Autocorrelación en Residuos
plt.figure(figsize=(12, 4))
plot_acf(residuos, lags=5)
plt.title('Gráfico de Autocorrelación en Residuos')
plt.xlabel('Lag')
plt.ylabel('ACF')
plt.show()

# Prueba de autocorrelación en residuos (Ljung-Box)
lag = 5  # Ajusta el número de rezagos a considerar
lb_test = acorr_ljungbox(residuos, lags=lag)
#lb_statistic, lb_pvalue = lb_test
print('Prueba de Ljung-Box para autocorrelación en residuos:')
for i in range(lag):
    print(f'Lag {i+1}: Estadística={lb_test.iloc[i, 0]:.2f}, p-valor={lb_test.iloc[i, 1]:.4f}')

for i in range(lag):
    if np.any(lb_test.iloc[i,1] < 0.05):
        print('Los residuos muestran autocorrelación significativa')
    else:
        print('Los residuos no muestran autocorrelación significativa')

# Histograma y Prueba de Normalidad (Shapiro-Wilk)
plt.figure(figsize=(12, 4))
plt.hist(residuos, bins=20, density=True, alpha=0.6, color='b', label='Histograma')
mu, sigma = stats.norm.fit(residuos)
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = stats.norm.pdf(x, mu, sigma)
plt.plot(x, p, 'k', linewidth=2, label='Distribución normal')
plt.title('Histograma y Prueba de Normalidad (Shapiro-Wilk)')
plt.xlabel('Residuos')
plt.ylabel('Frecuencia')
plt.legend()
plt.show()

shapiro_statistic, shapiro_pvalue = stats.shapiro(residuos)
print(f'Estadística Shapiro-Wilk: {shapiro_statistic:.4f}')
print(f'Valor p Shapiro-Wilk: {shapiro_pvalue:.4f}')

if shapiro_pvalue > 0.05:
    print('Los residuos siguen una distribución normal según la prueba Shapiro-Wilk')
else:
    print('Los residuos no siguen una distribución normal según la prueba Shapiro-Wilk')



arima_model()

get_auto_correlation_function()

if __name__ == "__main__":
    df = pd.read_excel("C:/Users/Usuario/Documents/Arima.xlsx")
    a = 1
