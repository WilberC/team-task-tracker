/* global React */
const { useState, useEffect } = React;

function Nav() {
  const [active, setActive] = useState("servicios");

  return (
    <>
      {/* Top bar — logo + CTA */}
      <div className="topbar">
        <a href="#top" className="logo-pill" aria-label="Jawinsa">
          <img src="../../assets/logo-placeholder.svg" alt="Jawinsa" style={{ height: 22 }} />
        </a>

        <div style={{ display: "flex", gap: 10 }}>
          <a href="tel:+5119991234" className="btn btn-ghost" style={{
            display: "inline-flex",
            padding: "12px 18px",
            fontSize: 13,
          }}>
            <i data-lucide="phone" width="14" height="14" {...{"stroke-width":"2"}}></i>
            Llamar
          </a>
          <a href="#contacto" className="cta-pill">
            Cotizar
            <i data-lucide="arrow-up-right" width="14" height="14" {...{"stroke-width":"2.2"}}></i>
          </a>
        </div>
      </div>

      {/* Pill nav — centered */}
      <nav className="pillnav">
        {[
          ["servicios", "Servicios"],
          ["industrial", "Industrial"],
          ["nosotros", "Nosotros"],
          ["noticias", "Noticias"],
          ["contacto", "Contacto"],
        ].map(([id, label]) => (
          <a
            key={id}
            href={`#${id}`}
            className={active === id ? "active" : ""}
            onClick={() => setActive(id)}
          >{label}</a>
        ))}
      </nav>

      {/* Side rail — only on extra-wide screens to avoid hero overlap */}
      <div className="siderail">
        <button className="ic" title="Diagnóstico">
          <i data-lucide="gauge" width="20" height="20" {...{"stroke-width":"1.75"}}></i>
        </button>
        <button className="ic" title="Repuestos">
          <i data-lucide="cog" width="20" height="20" {...{"stroke-width":"1.75"}}></i>
        </button>
        <button className="ic" title="Mantenimiento">
          <i data-lucide="wrench" width="20" height="20" {...{"stroke-width":"1.75"}}></i>
        </button>
        <button className="ic accent" title="WhatsApp">
          <i data-lucide="message-circle" width="20" height="20" {...{"stroke-width":"2"}}></i>
        </button>
      </div>
    </>
  );
}

window.Nav = Nav;
