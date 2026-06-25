/* global React */

function Footer() {
  return (
    <footer style={{ paddingTop: 24, paddingBottom: 24 }}>
      <div className="container">
        <div style={{
          background: "var(--ink)",
          color: "var(--paper)",
          borderRadius: 32,
          padding: "clamp(36px, 4vw, 56px)",
          position: "relative",
          overflow: "hidden",
        }}>
          {/* ambient amber */}
          <div style={{
            position: "absolute",
            right: -120, top: -120,
            width: 500, height: 500,
            background: "radial-gradient(circle, rgba(232,115,44,0.16), transparent 65%)",
            pointerEvents: "none",
          }} />

          <div className="footer-grid" style={{
            position: "relative", zIndex: 1,
            display: "grid",
            gridTemplateColumns: "1.6fr 1fr 1fr 1fr",
            gap: 48,
            paddingBottom: 48,
            borderBottom: "1px solid rgba(246,244,240,0.08)",
          }}>
            <div>
              <img src="../../assets/logo-placeholder-dark.svg" alt="Jawinsa" style={{ height: 38, marginBottom: 24 }} />
              <p style={{
                fontFamily: "var(--font-body)", fontSize: 14, lineHeight: 1.6,
                color: "var(--steel-300)", margin: 0, maxWidth: 320,
              }}>
                Taller multimarca e industrial. Reparación, mantenimiento y repuestos
                para vehículos, montacargas y grupos electrógenos.
              </p>
              <div style={{ display: "flex", gap: 10, marginTop: 28 }}>
                <SocialIcon icon="message-circle" />
                <SocialIcon icon="phone" />
                <SocialIcon icon="mail" />
                <SocialIcon icon="instagram" />
              </div>
            </div>

            <FooterCol title="Servicios" items={[
              "Línea automotriz", "Línea comercial", "Línea industrial",
              "Repuestos & consumibles", "Diagnóstico OBD-II",
            ]} />

            <FooterCol title="Empresa" items={[
              "Nosotros", "Equipo técnico", "Casos de éxito",
              "Licitaciones", "Trabaja con nosotros",
            ]} />

            <FooterCol title="Contacto" items={[
              "+51 999 123 456", "(01) 234-5678", "ventas@jawinsa.pe",
              "Av. Ejemplo 1234, Ate", "Lun–Sáb · 7:00 – 19:00",
            ]} mono />
          </div>

          <div style={{
            position: "relative", zIndex: 1,
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            paddingTop: 24,
            flexWrap: "wrap",
            gap: 16,
          }}>
            <div style={{
              fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--steel-500)",
              letterSpacing: "0.04em",
            }}>
              © 2026 Jawinsa S.A.C. · RUC 20XXXXXXXXX · Hecho en Lima
            </div>
            <div style={{ display: "flex", gap: 24 }}>
              <a href="#" style={{
                fontFamily: "var(--font-body)", fontSize: 12,
                color: "var(--steel-400)", textDecoration: "none",
              }}>Política de privacidad</a>
              <a href="#" style={{
                fontFamily: "var(--font-body)", fontSize: 12,
                color: "var(--steel-400)", textDecoration: "none",
              }}>Términos</a>
            </div>
          </div>
        </div>
      </div>

      <style>{`
        @media (max-width: 900px) {
          .footer-grid { grid-template-columns: 1fr 1fr !important; }
        }
        @media (max-width: 560px) {
          .footer-grid { grid-template-columns: 1fr !important; }
        }
      `}</style>
    </footer>
  );
}

function FooterCol({ title, items, mono }) {
  return (
    <div>
      <div style={{
        fontFamily: "var(--font-body)", fontWeight: 700, fontSize: 11,
        letterSpacing: "0.22em", textTransform: "uppercase",
        color: "var(--steel-400)", marginBottom: 18,
      }}>{title}</div>
      <ul style={{ listStyle: "none", padding: 0, margin: 0, display: "flex", flexDirection: "column", gap: 12 }}>
        {items.map(it => (
          <li key={it}>
            <a href="#" style={{
              fontFamily: mono ? "var(--font-mono)" : "var(--font-body)",
              fontSize: mono ? 13 : 14, color: "var(--steel-300)", textDecoration: "none",
            }}
            onMouseEnter={(e) => e.currentTarget.style.color = "var(--paper)"}
            onMouseLeave={(e) => e.currentTarget.style.color = "var(--steel-300)"}
            >{it}</a>
          </li>
        ))}
      </ul>
    </div>
  );
}

function SocialIcon({ icon }) {
  return (
    <a href="#" style={{
      width: 38, height: 38, borderRadius: 14,
      border: "1px solid rgba(246,244,240,0.12)",
      background: "rgba(246,244,240,0.04)",
      color: "var(--steel-300)",
      display: "flex", alignItems: "center", justifyContent: "center",
      textDecoration: "none",
      transition: "all 150ms var(--ease-out)",
    }}
    onMouseEnter={(e) => {
      e.currentTarget.style.background = "var(--accent)";
      e.currentTarget.style.color = "#fff";
      e.currentTarget.style.borderColor = "var(--accent)";
    }}
    onMouseLeave={(e) => {
      e.currentTarget.style.background = "rgba(246,244,240,0.04)";
      e.currentTarget.style.color = "var(--steel-300)";
      e.currentTarget.style.borderColor = "rgba(246,244,240,0.12)";
    }}
    >
      <i data-lucide={icon} width="16" height="16" {...{"stroke-width":"1.75"}}></i>
    </a>
  );
}

window.Footer = Footer;
