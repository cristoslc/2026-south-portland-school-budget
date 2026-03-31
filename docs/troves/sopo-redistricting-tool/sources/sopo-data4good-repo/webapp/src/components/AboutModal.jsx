export default function AboutModal({ onClose }) {
  return (
    <div className="modal-overlay" onClick={e => e.target === e.currentTarget && onClose()}>
      <div className="modal">
        <div className="modal-header">
          <h2>About This Tool</h2>
          <button className="modal-close" onClick={onClose}>×</button>
        </div>
        <div className="modal-body">
          <p>
            South Portland is considering closing one elementary school to address enrollment
            and budget pressures. This tool lets you explore what that could look like for
            families across the city — which neighborhoods would stay at their current school,
            which would move, how far kids would travel, and whether buildings would be over or
            under their enrollment limits.
          </p>
          <p>
            It's designed for anyone who wants to understand the tradeoffs — parents, city
            officials, school board members, and community members — no technical background
            needed.
          </p>

          <h3>The Four Scenarios</h3>
          <p>
            Each tab represents one school being closed. Skillin is not included because the
            remaining four schools don't have enough combined space for all current K–4 students.
          </p>
          <table>
            <thead>
              <tr><th>School</th><th>Capacity</th><th>Notes</th></tr>
            </thead>
            <tbody>
              <tr><td>Brown</td><td>260</td><td></td></tr>
              <tr><td>Dyer</td><td>240</td><td>Current PreK pilot site (29 students)</td></tr>
              <tr><td>Small</td><td>280</td><td></td></tr>
              <tr><td>Skillin</td><td>380</td><td>Not modeled as a closure option</td></tr>
              <tr><td>Kaler</td><td>240</td><td>Current PreK pilot site (29 students)</td></tr>
            </tbody>
          </table>

          <h3>Viewing Modes</h3>
          <p>
            Within each closure scenario, you can switch between three organizational models
            using the control bar on the map:
          </p>
          <ul>
            <li>
              <strong>Community Schools</strong> — each building houses all grades K–4, just
              like today. The PreK toggle lets you compare the current pilot (Dyer and Kaler
              only) against a full expansion where every open school hosts 29 PreK students.
            </li>
            <li>
              <strong>Grade Centers: PreK–1</strong> — two buildings become early-childhood
              centers serving PreK through 1st grade. The PreK toggle shows the difference
              between 29 and 58 PreK seats per center.
            </li>
            <li>
              <strong>Grade Centers: 2–4</strong> — the other two buildings serve Grades 2–4.
            </li>
          </ul>

          <h3>How Zone Boundaries Are Drawn</h3>
          <p>
            The suggested zone boundaries are generated automatically, not hand-drawn. The
            process prioritizes three things in order:
          </p>
          <ul>
            <li>
              <strong>Walkability first</strong> — neighborhoods within a 0.75-mile walk of a
              school are assigned there whenever possible. Walk distances use real sidewalk and
              road network data, so a highway or rail line between a home and a school will
              correctly show as non-walkable even if it looks close on a map.
            </li>
            <li>
              <strong>Capacity limits</strong> — no school is assigned more students than it
              can hold. If a neighborhood is walkable to a school that's already full, students
              are redirected to the nearest school with space.
            </li>
            <li>
              <strong>Neighborhood cohesion</strong> — nearby blocks are kept together in the
              same zone wherever possible, so neighbors and friends are more likely to end up
              at the same school.
            </li>
          </ul>
          <p>
            Student counts are estimates based on Census 2020 population data — they reflect
            where children likely live, not official enrollment records by home address.
          </p>

          <h3>What You Can Do</h3>
          <ul>
            <li>
              <strong>Explore scenarios</strong> — click the tabs at the top to switch between
              closure options and see how the map and statistics change.
            </li>
            <li>
              <strong>See who changes schools</strong> — click the <em>% Change Schools</em> button
              to highlight every block where students would move to a different school. A table
              shows each affected block with its original and proposed school.
            </li>
            <li>
              <strong>Adjust zone boundaries</strong> — click any colored block on the map to
              reassign it to a different school. Enrollment stats in the sidebar update instantly.
            </li>
            <li>
              <strong>Reset or export</strong> — use <strong>Reset to Base</strong> to undo your
              changes, or <strong>Download GeoJSON</strong> to save and share your modified zone map.
            </li>
            <li>
              <strong>Upload a plan</strong> — use the <strong>Upload Zones</strong> tab to load a
              zone file someone else created and see its live statistics.
            </li>
          </ul>

          <h3>A Note on the Numbers</h3>
          <p>
            Walk and drive distances reflect actual road network routing, not straight-line
            distances. However, they don't account for crossing guard locations, the quality
            of individual sidewalk segments, or family circumstances that affect how kids
            actually get to school. The enrollment figures are estimates — a family-level
            address dataset would produce more precise zone assignments.
          </p>
        </div>
      </div>
    </div>
  );
}
