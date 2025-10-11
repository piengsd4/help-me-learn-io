interface Goal {
    id: number;
    title: string;
    description: string;
    created_at?: string;
    updated_at?: string;
}

interface Instruction {
    id: number;
    goal: number;
    content: Record<string, string>;
    created_at?: string;
    updated_at?: string;
}

export type { Goal, Instruction };