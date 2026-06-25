/* global React */
const { useState, useEffect, useRef } = React;

function Contact() {
  const [sent, setSent] = useState(false);
  const [form, setForm] = useState({
    nombre: "", empresa: "", telefono: "", email: "",
    servicio: "Diagnóstico multimarca", mensaje: "",
  });

  const update = (k) => (e) => setForm({ ...form, [k]: e.target.value });
  const submit = (e) => {
    e.preventDefault();
    setSent(true);
    setTimeout(() => setSent(false), 4000);
  };

  const ref = useRef(null);
  const [inView, setInView] = useState(false);
  useEffect(() => {
    if (!ref.current) return;
    const io = new IntersectionObserver(([e]) => {
      if (e.isIntersecting) { setInView(true); io.disconnect(); }
    }, { threshold: 0.1 });
    io.observe(ref.current);
    return () => io.disconnect();
  }, []);

  return (
    <section id="contacto" className="section" ref={ref}>
      <div className="container">
        <div className={`reveal ${inView ? "in" : ""}`} style={{
          display: "grid",
          gridTemplateColumns: "1.2fr 1fr",
          gap: 14,
          alignItems: "stretch",
        }} >
          {/* Form */}
          <form onSubmit={submit} style={{
            background: "var(--paper-elevated)",
            border: "1px solid rgba(14,16,20,0.05)",
            borderRadius: 32,
            padding: "clamp(32px, 4vw, 48px)",
            display: "flex",
            flexDirection: "column",
            gap: 20,
            boxShadow: "var(--shadow-soft)",
          }} className="contact-form">
            <div>
              <div className="eyebrow"><span className="dot"></span>Contacto</div>
              <h2 style={{
                fontFamily: "var(--font-display)",
                fontWeight: 800,
                fontSize: "clamp(28px, 3vw, 44px)",
                lineHeight: 1.05,
                letterSpacing: "-0.025em",
                margin: "16px 0 0",
                color: "var(--fg-1)",
                textWrap: "balance",
              }}>
                Solicite su cotización.<br/>Respondemos en menos de 24 h.
              </h2>
            </div>

            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }} className="ftwo">
              <div className="field">
                <label>Nombre completo</label>
                <input type="text" required value={form.nombre} onChange={update("nombre")} placeholder="Andrés Tello" />
              </div>
              <div className="field">
                <label>Empresa (opcional)</label>
                <input type="text" value={form.empresa} onChange={update("empresa")} placeholder="Logística del Sur S.A." />
              </div>
            </div>

            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }} className="ftwo">
              <div className="field">
                <label>Teléfono / WhatsApp</label>
                <input type="tel" required value={form.telefono} onChange={update("telefono")} placeholder="+51 999 123 456" />
              </div>
              <div className="field">
                <label>Correo</label>
                <input type="email" required value={form.email} onChange={update("email")} placeholder="usted@empresa.com" />
              </div>
            </div>

            <div className="field">
              <label>Servicio requerido</label>
              <select value={form.servicio} onChange={update("servicio")}>
                <option>Diagnóstico multimarca</option>
                <option>Mantenimiento preventivo — auto particular</option>
                <option>Mantenimiento de flota (camiones / volquetes)</option>
                <option>Servicio técnico montacargas</option>
                <option>Servicio técnico grupos electrógenos</option>
                <option>Compra de repuestos / consumibles</option>
                <option>Licitación / contrato corporativo</option>
              </select>
            </div>

            <div className="field">
              <label>Detalle del servicio</label>
              <textarea value={form.mensaje} onChange={update("mensaje")} placeholder="Marca, modelo, año, kilometraje y descripción de la falla."></textarea>
            </div>

            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: 12, marginTop: 8 }}>
              <p style={{
                fontFamily: "var(--font-body)", fontSize: 12, color: "var(--fg-3)", margin: 0,
                maxWidth: 320,
              }}>Sin spam — respuesta en menos de 24 h hábiles.</p>
              <button type="submit" className="btn btn-primary btn-lg" disabled={sent}>
                {sent ? "Enviado ✓" : (
                  <>
                    Solicitar cotización
                    <i data-lucide="arrow-up-right" width="18" height="18" {...{"stroke-width":"2.2"}}></i>
                  </>
                )}
              </button>
            </div>
          </form>

          {/* Right column — contact cards */}
          <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
            <ContactCard
              icon="message-circle"
              eyebrow="WHATSAPP · MÁS RÁPIDO"
              title="+51 999 123 456"
              desc="Respuesta inmediata · Emergencias 24/7"
              href="https://wa.me/51999123456"
              theme="accent"
              big
            />
            <ContactCard
              icon="phone"
              eyebrow="LLAMAR"
              title="(01) 234-5678"
              desc="Lun – Sáb · 7:00 — 19:00"
              href="tel:+5112345678"
            />
            <ContactCard
              icon="map-pin"
              eyebrow="VISITAR EL TALLER"
              title="Av. Ejemplo 1234, Ate"
              desc="Lima, Perú · Estacionamiento para pesados"
              href="#"
              theme="dark"
            />
          </div>
        </div>
      </div>

      <style>{`
        @media (max-width: 900px) {
          #contacto .reveal > div, #contacto .reveal {
            grid-template-columns: 1fr !important;
          }
          #contacto .ftwo { grid-template-columns: 1fr !important; }
        }
      `}</style>
    </section>
  );
}

function ContactCard({ icon, eyebrow, title, desc, href, theme, big }) {
  const [hover, setHover] = useState(false);
  const accent = theme === "accent";
  const dark = theme === "dark";

  const bg = accent ? "var(--accent)" : dark ? "var(--ink)" : "var(--paper-elevated)";
  const fg = (accent || dark) ? "var(--paper)" : "var(--fg-1)";
  const sub = accent ? "rgba(255,255,255,0.9)" : dark ? "var(--steel-300)" : "var(--fg-2)";
  const ey = accent ? "rgba(255,255,255,0.78)" : dark ? "var(--steel-400)" : "var(--fg-3)";

  return (
    <a
      href={href}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{
        background: bg,
        color: fg,
        borderRadius: 28,
        padding: big ? "28px 32px" : "22px 26px",
        textDecoration: "none",
        display: "flex",
        gap: 18,
        alignItems: "flex-start",
        boxShadow: hover ? "var(--shadow-2)" : "var(--shadow-soft)",
        border: accent || dark ? "1px solid transparent" : "1px solid rgba(14,16,20,0.05)",
        transition: "box-shadow var(--dur-base) var(--ease-out), transform var(--dur-base) var(--ease-out)",
        transform: hover ? "translateY(-2px)" : "translateY(0)",
        position: "relative",
        overflow: "hidden",
        flex: big ? 1.4 : 1,
        minHeight: big ? 180 : "auto",
      }}
    >
      {accent && (
        <div style={{
          position: "absolute", inset: "auto -60px -60px auto",
          width: 220, height: 220,
          background: "radial-gradient(circle, rgba(255,255,255,0.18), transparent 70%)",
          pointerEvents: "none",
        }} />
      )}
      <div style={{
        width: big ? 56 : 44,
        height: big ? 56 : 44,
        flexShrink: 0,
        borderRadius: 16,
        background: accent || dark ? "rgba(255,255,255,0.18)" : "var(--ink)",
        color: accent || dark ? "#fff" : "var(--paper)",
        display: "flex", alignItems: "center", justifyContent: "center",
        position: "relative", zIndex: 1,
      }}>
        <i data-lucide={icon} width={big ? 24 : 20} height={big ? 24 : 20} {...{"stroke-width":"1.75"}}></i>
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: 6, position: "relative", zIndex: 1, flex: 1 }}>
        <div style={{
          fontFamily: "var(--font-body)", fontWeight: 700, fontSize: 10,
          letterSpacing: "0.22em", color: ey,
        }}>{eyebrow}</div>
        <div style={{
          fontFamily: "var(--font-display)", fontWeight: 800,
          fontSize: big ? 28 : 22, lineHeight: 1.05, letterSpacing: "-0.02em",
        }}>{title}</div>
        <div style={{
          fontFamily: "var(--font-body)", fontSize: 13, color: sub,
        }}>{desc}</div>
      </div>
      <div style={{
        width: 36, height: 36,
        borderRadius: "50%",
        background: accent || dark ? "rgba(255,255,255,0.16)" : "rgba(14,16,20,0.06)",
        color: accent || dark ? "#fff" : "var(--fg-1)",
        display: "flex", alignItems: "center", justifyContent: "center",
        position: "relative", zIndex: 1,
        flexShrink: 0,
        transition: "transform var(--dur-fast) var(--ease-out)",
        transform: hover ? "rotate(-45deg)" : "rotate(0deg)",
      }}>
        <i data-lucide="arrow-right" width="16" height="16" {...{"stroke-width":"2"}}></i>
      </div>
    </a>
  );
}

window.Contact = Contact;
