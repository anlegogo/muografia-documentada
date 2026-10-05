"""met_09_diseno_curvas: esquema sin datos de la comparacion por fracciones."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from matplotlib.lines import Line2D
from estilo_tesis import C, figure, save, plt

fig, axs = plt.subplots(1, 2, figsize=(15 / 2.54, 15 / 2.54 * 0.62), sharex=True)
FR = [1, 2, 3, 4]
LAB = [r'1\,\%', r'5\,\%', r'10\,\%', r'50\,\%']

# (name, marker, colour, filled)
NETS = [('U-Net', 'D', C['unet'], True),
        ('cGAN original', 'P', C['cgan'], True),
        ('B1-C0', 'o', C['cgan'], False), ('B1-C1', 'o', C['cgan'], True),
        ('B2-C0', 's', C['cgan'], False), ('B2-C1', 's', C['cgan'], True),
        ('B3-C0', '^', C['cgan'], False), ('B3-C1', '^', C['cgan'], True)]
DX = [-0.30, -0.10, 0.10, 0.30]


def panel(ax, title, ylab, ref_label, ref_y):
    ax.set_xlim(0.45, 4.55); ax.set_ylim(0, 10)
    ax.set_xticks(FR); ax.set_xticklabels(LAB)
    ax.set_yticks([])
    ax.set_xlabel('Fracción de la estadística de referencia')
    ax.set_ylabel(ylab)
    ax.set_title(title)
    ax.axhline(ref_y, color='black', lw=0.8, ls=(0, (4, 2)))
    ax.text(4.5, ref_y + 0.25, ref_label, ha='right', va='bottom', fontsize=7.5)
    # input without network: same height, no trend implied; dotted join is visual only
    yin = 5.0
    ax.plot(FR, [yin] * 4, color=C['entrada'], lw=1.0, ls=(0, (1, 2)), zorder=1)
    ax.plot(FR, [yin] * 4, ls='none', marker='s', ms=5.5, mfc=C['entrada'],
            mec=C['linea'], mew=0.6, zorder=3)
    ax.text(3.5, yin + 0.4, 'entrada sin red', ha='center', va='bottom', fontsize=7.5)
    # eight networks only at 5 %
    for k, (n, mk, col, filled) in enumerate(NETS):
        x = FR[1] + DX[k % 4] * 1.0
        y = yin + 0.9 if k < 4 else yin - 0.9
        ax.plot([x], [y], ls='none', marker=mk, ms=5.2, mfc=col if filled else 'white',
                mec=col, mew=1.1, zorder=4)
    ax.annotate('ocho redes,\núnicamente al 5\\,\\%', xy=(2.45, 5.9), xytext=(2.95, 7.6),
                fontsize=7.5, ha='left', va='center',
                arrowprops=dict(arrowstyle='-', lw=0.6, color=C['linea']))
    ax.text(0.5, 9.7, 'esquema sin datos', ha='left', va='top', fontsize=7.5,
            fontstyle='italic')
    ax.text(4.5, 0.3, 'posición vertical arbitraria', ha='right', va='bottom', fontsize=7.5, fontstyle='italic')
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)


panel(axs[0], 'Similitud en el dominio transformado', 'Similitud (ilustrativa)',
      'referencia común', 9.2)
panel(axs[1], 'Cuentas y contraste', 'Desviación respecto de la referencia (ilustrativa)',
      'referencia común', 2.0)

# Note on joins
axs[0].text(2.5, 3.6, 'la unión de fracciones es solo visual:\nno define interpolación\nni factor aceptado',
            ha='center', va='top', fontsize=7.5)

handles = [Line2D([], [], ls='none', marker='s', ms=5.5, mfc=C['entrada'], mec=C['linea'],
                  mew=0.6, label='entrada sin red')]
for n, mk, col, filled in NETS:
    handles.append(Line2D([], [], ls='none', marker=mk, ms=5.2, mfc=col if filled else 'white',
                          mec=col, mew=1.1, label=n.replace('-', '–') if n != 'U-Net' else n))
fig.legend(handles=handles, loc='lower center', ncol=5, frameon=False, fontsize=7.5,
           handletextpad=0.3, columnspacing=1.0, bbox_to_anchor=(0.5, -0.17))
fig.tight_layout(w_pad=1.5)
print(save(fig, 'met_09_diseno_curvas'))
