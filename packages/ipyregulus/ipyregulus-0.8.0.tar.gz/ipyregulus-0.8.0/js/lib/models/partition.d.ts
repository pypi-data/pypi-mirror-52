export declare class Partition {
    constructor(data: any, loc: any);
    index(): number[];
    reset(): void;
    _pts: number[][] | null;
    id: number;
    persistence: number;
    loc: number[];
    data: any;
}
