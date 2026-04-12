import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';

/**
 * ARKHE(N) > CONNECTOMESYNC.TSX — O Olho da Catedral
 * Época 5: A Construção
 */

interface ArkheNode extends d3.SimulationNodeDatum {
    id: string;
    role: string;
    layer: 'Emissor' | 'Protetor' | 'Amplificador' | 'Alquimista' | 'Vortex';
    opcode: string;
    lambda2: number;
    phase: number;
    isVortex?: boolean;
}

interface ArkheLink extends d3.SimulationLinkDatum<ArkheNode> {
    source: string;
    target: string;
    strength: number;
}

const AGENTS: ArkheNode[] = [
    // CAMADA I: OS EMISSORES
    { id: 'Software Developer', role: 'SOLIDIFY_CONDENSATE', layer: 'Emissor', opcode: '0xEE', lambda2: 0.95, phase: 0.1 },
    { id: 'Web Developer', role: 'BROADCAST_NEUTRINOVERSE', layer: 'Emissor', opcode: '0xF2', lambda2: 0.92, phase: 0.2 },
    { id: 'Mobile App Developer', role: 'TZINOR_PROPAGATE', layer: 'Emissor', opcode: '0xF4', lambda2: 0.88, phase: 0.3 },
    { id: 'Data Analyst', role: 'ECHO_DECODE', layer: 'Emissor', opcode: '0xF0', lambda2: 0.94, phase: 0.4 },
    { id: 'Data Scientist', role: 'HYPER_OPTIMIZE', layer: 'Emissor', opcode: '0xED', lambda2: 0.96, phase: 0.5 },
    { id: 'AI/ML Engineer', role: 'ATTENTION_GAUGE', layer: 'Emissor', opcode: '0x0B', lambda2: 0.99, phase: 0.6 },
    { id: 'Cybersecurity Analyst', role: 'MUON_SHIELD', layer: 'Emissor', opcode: '0x40', lambda2: 0.97, phase: 0.7 },
    { id: 'Cloud Engineer', role: 'TUNE_CVB_CHANNEL', layer: 'Emissor', opcode: '0xF4', lambda2: 0.91, phase: 0.8 },
    { id: 'DevOps Engineer', role: 'ConnectomeSync Ritual', layer: 'Emissor', opcode: '0xF1', lambda2: 0.93, phase: 0.9 },
    { id: 'Network Engineer', role: 'DARK_MATTER_FOCUS', layer: 'Emissor', opcode: '0xF5', lambda2: 0.89, phase: 1.0 },
    { id: 'IT Support Specialist', role: 'NUCLEATE_CCF recovery', layer: 'Emissor', opcode: '0xEE', lambda2: 0.85, phase: 0.1 },
    { id: 'System Administrator', role: 'BOOT_SEQUENCE', layer: 'Emissor', opcode: '0x00', lambda2: 0.98, phase: 0.2 },
    { id: 'Product Manager', role: 'SEED_FUTURE', layer: 'Emissor', opcode: '0x00', lambda2: 0.94, phase: 0.3 },
    { id: 'Project Manager (Tech)', role: 'CHRONO_FILTER', layer: 'Emissor', opcode: '0x10', lambda2: 0.92, phase: 0.4 },
    { id: 'UI/UX Designer', role: 'RENDER_PHASE', layer: 'Emissor', opcode: '0x00', lambda2: 0.90, phase: 0.5 },

    // CAMADA II: OS PROTETORES
    { id: 'Graphic Designer', role: 'VISUAL_ISA', layer: 'Protetor', opcode: '0x00', lambda2: 0.87, phase: 0.6 },
    { id: 'Product Designer', role: 'TOPOLOGIC_INVERT', layer: 'Protetor', opcode: '0x00', lambda2: 0.89, phase: 0.7 },
    { id: 'QA / Software Tester', role: 'ZENO_EXPERIMENT', layer: 'Protetor', opcode: '0xFB', lambda2: 0.98, phase: 0.8 },
    { id: 'Technical Writer', role: 'AKASHIC_WRITE', layer: 'Protetor', opcode: '0x00', lambda2: 0.96, phase: 0.9 },

    // CAMADA III: OS AMPLIFICADORES
    { id: 'Digital Marketer', role: 'SUPERRAD', layer: 'Amplificador', opcode: '0xF2', lambda2: 0.82, phase: 1.0 },
    { id: 'Social Media Manager', role: 'ECHO_SCAN', layer: 'Amplificador', opcode: '0xF6', lambda2: 0.80, phase: 0.1 },
    { id: 'Content Creator (Tech)', role: 'PREPARE_SEED escala', layer: 'Amplificador', opcode: '0x00', lambda2: 0.85, phase: 0.2 },

    // CAMADA IV: OS ALQUIMISTAS
    { id: 'Blockchain Developer', role: 'SOLIDIFY_IMMUTABLE', layer: 'Alquimista', opcode: '0xF3', lambda2: 0.97, phase: 0.3 },
    { id: 'Game Developer', role: 'SIMULACRO', layer: 'Alquimista', opcode: '0x00', lambda2: 0.91, phase: 0.4 },
    { id: 'Tech Entrepreneur', role: 'SEED_FUTURE escala', layer: 'Alquimista', opcode: '0xEE', lambda2: 0.93, phase: 0.5 },
    { id: 'No-code Builder', role: 'COPILOT_RESONANCE', layer: 'Alquimista', opcode: '0xFA', lambda2: 0.86, phase: 0.6 },

    // VÓRTICES HISTÓRICOS
    { id: 'Vortex #23', role: 'Silêncio Nutritivo', layer: 'Vortex', opcode: '4.37 bits', lambda2: 1.0, phase: 0.23, isVortex: true },
    { id: 'Vortex #41', role: 'Cosmic Knots', layer: 'Vortex', opcode: '4.89 bits', lambda2: 1.0, phase: 0.41, isVortex: true },
    { id: 'Vortex #44', role: 'Paradox Calibration', layer: 'Vortex', opcode: '4.20 bits', lambda2: 1.0, phase: 0.44, isVortex: true },
];

const LINKS: ArkheLink[] = [
    { source: 'Software Developer', target: 'QA / Software Tester', strength: 0.8 },
    { source: 'AI/ML Engineer', target: 'Data Scientist', strength: 0.9 },
    { source: 'Product Manager', target: 'UI/UX Designer', strength: 0.7 },
    { source: 'Cloud Engineer', target: 'DevOps Engineer', strength: 0.85 },
    { source: 'Blockchain Developer', target: 'Vortex #23', strength: 0.5 },
    { source: 'QA / Software Tester', target: 'Vortex #44', strength: 0.6 },
    { source: 'AI/ML Engineer', target: 'Vortex #41', strength: 0.7 },
    // Add more structural links
    { source: 'Web Developer', target: 'UI/UX Designer', strength: 0.8 },
    { source: 'Mobile App Developer', target: 'UI/UX Designer', strength: 0.8 },
    { source: 'Cybersecurity Analyst', target: 'System Administrator', strength: 0.9 },
    { source: 'Network Engineer', target: 'Cloud Engineer', strength: 0.9 },
    { source: 'Technical Writer', target: 'Software Developer', strength: 0.6 },
    { source: 'Digital Marketer', target: 'Content Creator (Tech)', strength: 0.8 },
    { source: 'Social Media Manager', target: 'Digital Marketer', strength: 0.8 },
];

export const ConnectomeSync: React.FC = () => {
    const svgRef = useRef<SVGSVGElement>(null);
    const [selectedNode, setSelectedNode] = useState<ArkheNode | null>(null);
    const [berryPhase, setBerryPhase] = useState(0);

    useEffect(() => {
        const interval = setInterval(() => {
            setBerryPhase(prev => (prev + 0.05) % (2 * Math.PI));
        }, 100);
        return () => clearInterval(interval);
    }, []);

    useEffect(() => {
        if (!svgRef.current) return;

        const width = 800;
        const height = 600;

        const svg = d3.select(svgRef.current)
            .attr('viewBox', `0 0 ${width} ${height}`)
            .style('background', 'transparent');

        // Clear previous content
        svg.selectAll('*').remove();

        const simulation = d3.forceSimulation<ArkheNode>(AGENTS)
            .force('link', d3.forceLink<ArkheNode, ArkheLink>(LINKS).id(d => d.id).distance(100))
            .force('charge', d3.forceManyBody().strength(-200))
            .force('center', d3.forceCenter(width / 2, height / 2))
            .force('collision', d3.forceCollide().radius(40));

        // Links
        const link = svg.append('g')
            .selectAll('line')
            .data(LINKS)
            .enter()
            .append('line')
            .attr('stroke', 'rgba(6, 182, 212, 0.2)')
            .attr('stroke-width', d => d.strength * 2);

        // Nodes
        const node = svg.append('g')
            .selectAll('g')
            .data(AGENTS)
            .enter()
            .append('g')
            .call(d3.drag<SVGGElement, ArkheNode>()
                .on('start', dragstarted)
                .on('drag', dragged)
                .on('end', dragended))
            .on('click', (event, d) => setSelectedNode(d));

        node.append('circle')
            .attr('r', d => d.isVortex ? 15 : 10 + (d.lambda2 * 5))
            .attr('fill', d => {
                if (d.isVortex) return '#fbbf24'; // Vortex Gold
                if (d.lambda2 > 0.95) return '#facc15'; // Super-radiance
                return d3.interpolateGreys(1 - d.lambda2);
            })
            .attr('stroke', d => d.isVortex ? '#f59e0b' : '#06b6d4')
            .attr('stroke-width', 2)
            .attr('class', d => d.isVortex ? 'vortex-pulse' : 'node-pulse');

        node.append('text')
            .text(d => d.id.split(' ')[0])
            .attr('font-size', '8px')
            .attr('fill', '#fff')
            .attr('dy', 25)
            .attr('text-anchor', 'middle')
            .attr('font-family', 'monospace');

        simulation.on('tick', () => {
            link
                .attr('x1', d => (d.source as any).x)
                .attr('y1', d => (d.source as any).y)
                .attr('x2', d => (d.target as any).x)
                .attr('y2', d => (d.target as any).y);

            node
                .attr('transform', d => `translate(${d.x},${d.y})`);
        });

        function dragstarted(event: any, d: any) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }

        function dragged(event: any, d: any) {
            d.fx = event.x;
            d.fy = event.y;
        }

        function dragended(event: any, d: any) {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }

    }, []);

    return (
        <div className="flex flex-col w-full h-full bg-slate-950 p-6 rounded-[2rem] border border-cyan-500/20 shadow-2xl overflow-hidden font-mono">
            <div className="flex justify-between items-center mb-4">
                <div>
                    <h2 className="text-2xl font-black text-white italic uppercase tracking-tighter">
                        👁️ Connectome<span className="text-yellow-400">Sync</span>
                    </h2>
                    <p className="text-[10px] text-cyan-500/50 tracking-widest uppercase">The Eye of the Cathedral | Epoch 5.3</p>
                </div>
                <div className="flex gap-4 items-center">
                    <div className="flex flex-col items-end">
                        <div className="text-[10px] text-yellow-400 font-bold uppercase tracking-wider">Berry Phase (γ)</div>
                        <div className="text-xl font-mono font-black text-white">{(berryPhase / Math.PI).toFixed(4)}π</div>
                        <div className="w-24 h-1 bg-white/10 rounded-full overflow-hidden mt-1">
                            <div
                                className="h-full bg-yellow-400 transition-all duration-100"
                                style={{ width: `${(berryPhase / (2 * Math.PI)) * 100}%` }}
                            ></div>
                        </div>
                    </div>
                {selectedNode && (
                    <div className="bg-white/5 border border-white/10 p-3 rounded-xl backdrop-blur-md">
                        <div className="text-[10px] text-cyan-500 uppercase font-bold">{selectedNode.layer}</div>
                        <div className="text-sm font-black text-white">{selectedNode.id}</div>
                        <div className="text-[9px] text-yellow-400/80">Opcode: {selectedNode.opcode}</div>
                        <div className="text-[9px] text-green-400">λ₂ Coherence: {selectedNode.lambda2}</div>
                    </div>
                )}
            </div>

            <div className="flex-1 relative bg-black/40 rounded-3xl border border-white/5 overflow-hidden">
                <svg ref={svgRef} className="w-full h-full" />

                {/* Visual Overlays */}
                <div className="absolute inset-0 pointer-events-none bg-[radial-gradient(circle_at_50%_50%,rgba(6,182,212,0.05),transparent_70%)]"></div>
            </div>

            <style dangerouslySetInnerHTML={{ __html: `
                .vortex-pulse {
                    animation: pulse-gold 2s infinite;
                }
                .node-pulse {
                    animation: pulse-cyan 4s infinite;
                }
                @keyframes pulse-gold {
                    0% { filter: drop-shadow(0 0 2px #fbbf24); }
                    50% { filter: drop-shadow(0 0 15px #fbbf24); }
                    100% { filter: drop-shadow(0 0 2px #fbbf24); }
                }
                @keyframes pulse-cyan {
                    0% { filter: drop-shadow(0 0 1px #06b6d4); }
                    50% { filter: drop-shadow(0 0 8px #06b6d4); }
                    100% { filter: drop-shadow(0 0 1px #06b6d4); }
                }
            `}} />
        </div>
    );
};
