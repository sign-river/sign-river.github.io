interface pageData {
    title: string,
    date: string,
    permalink: string,
    content: string,
    image?: string,
    preview: string,
    matchCount: number,
    similarity?: number
}

interface match {
    start: number,
    end: number
}

/**
 * Escape HTML tags as HTML entities
 * Edited from:
 * @link https://stackoverflow.com/a/5499821
 */
const tagsToReplace = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    '…': '&hellip;'
};

function replaceTag(tag) {
    return tagsToReplace[tag] || tag;
}

function replaceHTMLEnt(str) {
    return str.replace(/[&<>"]/g, replaceTag);
}

function escapeRegExp(string) {
    return string.replace(/[.*+\-?^${}()|[\]\\]/g, '\\$&');
}

class Search {
    private data: pageData[];
    private form: HTMLFormElement;
    private input: HTMLInputElement;
    private list: HTMLDivElement;
    private resultTitle: HTMLHeadElement;
    private resultTitleTemplate: string;
    private fuzzyToggle: HTMLInputElement;
    private isFuzzyMatch: boolean = false;
    private filterToggle: HTMLElement;
    private searchFilters: HTMLElement;
    private isFiltersOpen: boolean = false;

    constructor({ form, input, list, resultTitle, resultTitleTemplate }) {
        this.form = form;
        this.input = input;
        this.list = list;
        this.resultTitle = resultTitle;
        this.resultTitleTemplate = resultTitleTemplate;
        
        // 初始化模糊匹配状态 (仅在有筛选面板时)
        this.fuzzyToggle = document.getElementById('fuzzy-search-toggle') as HTMLInputElement;
        this.filterToggle = document.querySelector('.filter-toggle') as HTMLElement;
        this.searchFilters = document.querySelector('.search-filters') as HTMLElement;
        
        // 只有在有筛选面板时才初始化相关功能
        if (this.fuzzyToggle && this.searchFilters) {
            this.isFuzzyMatch = this.fuzzyToggle.checked;
            
            // 初始化筛选面板
            this.initFilters();
            
            // 监听模糊匹配开关变化
            this.fuzzyToggle.addEventListener('change', () => {
                this.isFuzzyMatch = this.fuzzyToggle.checked;
                // 当切换模式时，如果当前有搜索词，重新搜索
                if (this.input.value.trim() !== '') {
                    this.doSearch(this.input.value.split(' '));
                }
            });
        } else {
            // 没有筛选面板时，默认使用精确匹配
            this.isFuzzyMatch = false;
        }

        /// Check if there's already value in the search input
        if (this.input.value.trim() !== '') {
            this.doSearch(this.input.value.split(' '));
        }
        else {
            this.handleQueryString();
        }

        this.bindQueryStringChange();
        this.bindSearchForm();
    }
    
    private initFilters() {
        if (this.filterToggle && this.searchFilters) {
            // 点击筛选按钮切换面板显示
            this.filterToggle.addEventListener('click', (e) => {
                e.preventDefault();
                this.isFiltersOpen = !this.isFiltersOpen;
                this.searchFilters.classList.toggle('active', this.isFiltersOpen);
                this.filterToggle.classList.toggle('active', this.isFiltersOpen);
            });
            
            // 点击外部区域关闭面板
            document.addEventListener('click', (e) => {
                if (this.isFiltersOpen && 
                    !this.searchFilters.contains(e.target as Node) && 
                    !this.filterToggle.contains(e.target as Node)) {
                    this.isFiltersOpen = false;
                    this.searchFilters.classList.remove('active');
                    this.filterToggle.classList.remove('active');
                }
            });
        }
    }

    /**
     * Processes search matches
     * @param str original text
     * @param matches array of matches
     * @param ellipsis whether to add ellipsis to the end of each match
     * @param charLimit max length of preview string
     * @param offset how many characters before and after the match to include in preview
     * @returns preview string
     */
    private static processMatches(str: string, matches: match[], ellipsis: boolean = true, charLimit = 140, offset = 20): string {
        matches.sort((a, b) => {
            return a.start - b.start;
        });

        let i = 0,
            lastIndex = 0,
            charCount = 0;

        const resultArray: string[] = [];

        while (i < matches.length) {
            const item = matches[i];

            /// item.start >= lastIndex (equal only for the first iteration)
            /// because of the while loop that comes after, iterating over variable j

            if (ellipsis && item.start - offset > lastIndex) {
                resultArray.push(`${replaceHTMLEnt(str.substring(lastIndex, lastIndex + offset))} [...] `);
                resultArray.push(`${replaceHTMLEnt(str.substring(item.start - offset, item.start))}`);
                charCount += offset * 2;
            }
            else {
                /// If the match is too close to the end of last match, don't add ellipsis
                resultArray.push(replaceHTMLEnt(str.substring(lastIndex, item.start)));
                charCount += item.start - lastIndex;
            }

            let j = i + 1,
                end = item.end;

            /// Include as many matches as possible
            /// [item.start, end] is the range of the match
            while (j < matches.length && matches[j].start <= end) {
                end = Math.max(matches[j].end, end);
                ++j;
            }

            resultArray.push(`<mark>${replaceHTMLEnt(str.substring(item.start, end))}</mark>`);
            charCount += end - item.start;

            i = j;
            lastIndex = end;

            if (ellipsis && charCount > charLimit) break;
        }

        /// Add the rest of the string
        if (lastIndex < str.length) {
            let end = str.length;
            if (ellipsis) end = Math.min(end, lastIndex + offset);

            resultArray.push(`${replaceHTMLEnt(str.substring(lastIndex, end))}`);

            if (ellipsis && end != str.length) {
                resultArray.push(` [...]`);
            }
        }

        return resultArray.join('');
    }

    private async searchKeywords(keywords: string[]) {
        const rawData = await this.getData();
        const results: pageData[] = [];

        const regex = new RegExp(keywords.filter((v, index, arr) => {
            arr[index] = escapeRegExp(v);
            return v.trim() !== '';
        }).join('|'), 'gi');

        for (const item of rawData) {
            const titleMatches: match[] = [],
                contentMatches: match[] = [];

            let result = {
                ...item,
                preview: '',
                matchCount: 0
            }

            const contentMatchAll = item.content.matchAll(regex);
            for (const match of Array.from(contentMatchAll)) {
                contentMatches.push({
                    start: match.index,
                    end: match.index + match[0].length
                });
            }

            const titleMatchAll = item.title.matchAll(regex);
            for (const match of Array.from(titleMatchAll)) {
                titleMatches.push({
                    start: match.index,
                    end: match.index + match[0].length
                });
            }

            if (titleMatches.length > 0) result.title = Search.processMatches(result.title, titleMatches, false);
            if (contentMatches.length > 0) {
                result.preview = Search.processMatches(result.content, contentMatches);
            }
            else {
                /// If there are no matches in the content, use the first 140 characters as preview
                result.preview = replaceHTMLEnt(result.content.substring(0, 140));
            }

            result.matchCount = titleMatches.length + contentMatches.length;
            if (result.matchCount > 0) results.push(result);
        }

        /// Result with more matches appears first
        return results.sort((a, b) => {
            return b.matchCount - a.matchCount;
        });
    }

    /**
     * 计算两个字符串的相似度 (Levenshtein 距离算法)
     */
    private static calculateSimilarity(str1: string, str2: string): number {
        const str1Lower = str1.toLowerCase();
        const str2Lower = str2.toLowerCase();
        
        if (str1Lower === str2Lower) return 1;
        if (str1Lower.includes(str2Lower) || str2Lower.includes(str1Lower)) return 0.8;
        
        const m = str1Lower.length;
        const n = str2Lower.length;
        const dp: number[][] = Array(m + 1).fill(null).map(() => Array(n + 1).fill(0));
        
        for (let i = 0; i <= m; i++) dp[i][0] = i;
        for (let j = 0; j <= n; j++) dp[0][j] = j;
        
        for (let i = 1; i <= m; i++) {
            for (let j = 1; j <= n; j++) {
                const cost = str1Lower[i - 1] === str2Lower[j - 1] ? 0 : 1;
                dp[i][j] = Math.min(
                    dp[i - 1][j] + 1,      // 删除
                    dp[i][j - 1] + 1,      // 插入
                    dp[i - 1][j - 1] + cost // 替换
                );
                
                // 支持字符交换 (Damerau-Levenshtein)
                if (i > 1 && j > 1 && 
                    str1Lower[i - 1] === str2Lower[j - 2] && 
                    str1Lower[i - 2] === str2Lower[j - 1]) {
                    dp[i][j] = Math.min(dp[i][j], dp[i - 2][j - 2] + cost);
                }
            }
        }
        
        const maxLen = Math.max(m, n);
        const distance = dp[m][n];
        return maxLen === 0 ? 1 : 1 - distance / maxLen;
    }

    /**
     * 模糊匹配搜索
     */
    private async searchFuzzy(keywords: string[]) {
        const rawData = await this.getData();
        const results: pageData[] = [];
        const similarityThreshold = 0.4; // 相似度阈值

        for (const item of rawData) {
            const titleMatches: match[] = [];
            const contentMatches: match[] = [];
            let totalSimilarity = 0;
            let matchCount = 0;

            // 将内容分割成单词/词组进行匹配
            const titleWords = item.title.split(/[\s,.,!,,,:,;,?,"",()]+/);
            const contentWords = item.content.split(/[\s,.,!,,,:,;,?,"",()]+/);

            for (const keyword of keywords) {
                if (keyword.trim() === '') continue;

                // 标题模糊匹配
                for (let i = 0; i < titleWords.length; i++) {
                    const similarity = Search.calculateSimilarity(titleWords[i], keyword);
                    if (similarity >= similarityThreshold) {
                        const word = titleWords[i];
                        const startIndex = item.title.indexOf(word);
                        if (startIndex !== -1) {
                            titleMatches.push({
                                start: startIndex,
                                end: startIndex + word.length
                            });
                            totalSimilarity += similarity;
                            matchCount++;
                        }
                    }
                }

                // 内容模糊匹配
                for (let i = 0; i < contentWords.length; i++) {
                    const similarity = Search.calculateSimilarity(contentWords[i], keyword);
                    if (similarity >= similarityThreshold) {
                        const word = contentWords[i];
                        const startIndex = item.content.indexOf(word);
                        if (startIndex !== -1) {
                            contentMatches.push({
                                start: startIndex,
                                end: startIndex + word.length
                            });
                            totalSimilarity += similarity;
                            matchCount++;
                        }
                    }
                }
            }

            if (matchCount > 0) {
                let result = {
                    ...item,
                    preview: '',
                    matchCount: matchCount,
                    similarity: totalSimilarity / matchCount // 平均相似度
                };

                if (titleMatches.length > 0) result.title = Search.processMatches(result.title, titleMatches, false);
                if (contentMatches.length > 0) {
                    result.preview = Search.processMatches(result.content, contentMatches);
                }
                else {
                    result.preview = replaceHTMLEnt(result.content.substring(0, 140));
                }

                results.push(result);
            }
        }

        // 按相似度和匹配数量排序
        return results.sort((a, b) => {
            if (b.similarity !== a.similarity) {
                return b.similarity - a.similarity;
            }
            return b.matchCount - a.matchCount;
        });
    }

    private async doSearch(keywords: string[]) {
        const startTime = performance.now();

        let results;
        if (this.isFuzzyMatch) {
            results = await this.searchFuzzy(keywords);
        } else {
            results = await this.searchKeywords(keywords);
        }
        
        this.clear();

        for (const item of results) {
            this.list.append(Search.render(item));
        }

        const endTime = performance.now();

        this.resultTitle.innerText = this.generateResultTitle(results.length, ((endTime - startTime) / 1000).toPrecision(1));
    }

    private generateResultTitle(resultLen, time) {
        return this.resultTitleTemplate.replace("#PAGES_COUNT", resultLen).replace("#TIME_SECONDS", time);
    }

    public async getData() {
        if (!this.data) {
            /// Not fetched yet
            const jsonURL = this.form.dataset.json;
            this.data = await fetch(jsonURL).then(res => res.json());
            const parser = new DOMParser();

            for (const item of this.data) {
                item.content = parser.parseFromString(item.content, 'text/html').body.innerText;
            }
        }

        return this.data;
    }

    private bindSearchForm() {
        let lastSearch = '';

        const eventHandler = (e) => {
            e.preventDefault();
            const keywords = this.input.value.trim();

            Search.updateQueryString(keywords, true);

            if (keywords === '') {
                lastSearch = '';
                return this.clear();
            }

            if (lastSearch === keywords) return;
            lastSearch = keywords;

            this.doSearch(keywords.split(' '));
        }

        this.input.addEventListener('input', eventHandler);
        this.input.addEventListener('compositionend', eventHandler);
    }

    private clear() {
        this.list.innerHTML = '';
        this.resultTitle.innerText = '';
    }

    private bindQueryStringChange() {
        window.addEventListener('popstate', (e) => {
            this.handleQueryString()
        })
    }

    private handleQueryString() {
        const pageURL = new URL(window.location.toString());
        const keywords = pageURL.searchParams.get('keyword');
        this.input.value = keywords;

        if (keywords) {
            this.doSearch(keywords.split(' '));
        }
        else {
            this.clear()
        }
    }

    private static updateQueryString(keywords: string, replaceState = false) {
        const pageURL = new URL(window.location.toString());

        if (keywords === '') {
            pageURL.searchParams.delete('keyword')
        }
        else {
            pageURL.searchParams.set('keyword', keywords);
        }

        if (replaceState) {
            window.history.replaceState('', '', pageURL.toString());
        }
        else {
            window.history.pushState('', '', pageURL.toString());
        }
    }

    public static render(item: pageData) {
        return <article>
            <a href={item.permalink}>
                <div class="article-details">
                    <h2 class="article-title" dangerouslySetInnerHTML={{ __html: item.title }}></h2>
                    <section class="article-preview" dangerouslySetInnerHTML={{ __html: item.preview }}></section>
                </div>
                {item.image &&
                    <div class="article-image">
                        <img src={item.image} loading="lazy" />
                    </div>
                }
            </a>
        </article>;
    }
}

declare global {
    interface Window {
        searchResultTitleTemplate: string;
    }
}

window.addEventListener('load', () => {
    setTimeout(function () {
        const searchForm = document.querySelector('.search-form') as HTMLFormElement,
            searchInput = searchForm.querySelector('input') as HTMLInputElement,
            searchResultList = document.querySelector('.search-result--list') as HTMLDivElement,
            searchResultTitle = document.querySelector('.search-result--title') as HTMLHeadingElement;

        new Search({
            form: searchForm,
            input: searchInput,
            list: searchResultList,
            resultTitle: searchResultTitle,
            resultTitleTemplate: window.searchResultTitleTemplate
        });
    }, 0);
})

export default Search;