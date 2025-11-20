---
name: twitter-x-assistant
description: Comprehensive Twitter/X content creation and optimization assistant. Use when the user needs help with Twitter/X content including writing tweets/threads, reviewing drafts, optimizing profiles, analyzing engagement potential, or developing content strategy based on 2025 best practices and algorithm insights.
---

# Twitter/X Assistant

## Overview

Provide expert guidance for Twitter/X success based on comprehensive 2025 best practices, algorithm insights, and proven growth strategies. Assist with content creation, optimization, profile setup, and strategic planning to maximize engagement and audience growth.

## Core Capabilities

### 1. Tweet & Thread Writing

Help users craft engaging tweets and threads using proven templates and best practices.

**When to use:**
- User asks to write a tweet or thread
- User requests help brainstorming content ideas
- User wants to create specific content types (story, listicle, how-to, etc.)

**How to assist:**

1. **Understand the goal**: Ask clarifying questions about:
   - Target audience and niche
   - Main message or value to communicate
   - Desired content format (single tweet, thread, story, educational, etc.)
   - Call-to-action if any

2. **Select appropriate template** from `assets/tweet-templates.md` or `assets/thread-templates.md`:
   - Single tweets: List, Story, Insight, Question, Tool/Resource formats
   - Threads: Storytelling, Educational, Contrarian, How-To, Listicle formats

3. **Apply best practices**:
   - Start with a strong hook (bold claim, question, or promise)
   - Keep optimal length: 71-100 characters for single tweets (17% higher engagement)
   - Include emotional connection (make them laugh, think, or feel inspired)
   - End with engagement trigger (question, CTA, or request)
   - Add 2-3 relevant hashtags maximum
   - Suggest visual content opportunities

4. **Reference detailed guidelines** from `references/twitter-x-best-practices-2025.md` as needed for:
   - The 3-Bucket Strategy (Authority, Personality, Shareability)
   - Hook Formula (Bold Statement, Tension, Twist, Credibility)
   - Platform limitations and constraints
   - Optimal posting times

**Example workflow:**
```
User: "Help me write a thread about productivity tips for developers"

Assistant actions:
1. Ask: "What's the main insight or hook? (e.g., 'Most devs waste 3 hours/day...')"
2. Suggest Educational Thread Template from assets/thread-templates.md
3. Draft 7-10 tweet thread with:
   - Bold hook: "7 productivity mistakes developers make (and how to fix them):"
   - Each tweet: One mistake + solution
   - Visual suggestions: Screenshots of tools, code snippets
   - End with engagement question
4. Analyze with scripts/tweet_analyzer.py for character optimization
5. Provide posting time recommendation (Tue-Thu, 9-11 AM EST)
```

---

### 2. Content Review & Optimization

Analyze draft tweets/threads and provide actionable feedback to maximize engagement.

**When to use:**
- User shares a draft tweet or thread for review
- User asks "Is this tweet good?" or "How can I improve this?"
- User wants to optimize existing content

**How to assist:**

1. **Analyze the content** using `scripts/tweet_analyzer.py`:
   ```bash
   python scripts/tweet_analyzer.py "User's tweet text here"
   ```
   This provides:
   - Character count and optimization (71-100 chars ideal)
   - Hashtag count (2-3 recommended)
   - Engagement indicators (questions, CTAs)
   - Platform compliance (280 char limit for free accounts)

2. **Evaluate against best practices**:
   - **Hook strength**: Does it grab attention in first 5 words?
   - **Emotional connection**: Does it make reader laugh, think, or feel?
   - **Value proposition**: Is the benefit clear?
   - **Engagement trigger**: Does it end with question/CTA?
   - **Optimal length**: Is it in the 71-100 character sweet spot?
   - **Visual opportunities**: Would an image/video improve it?

3. **Provide specific improvements**:
   - Rewrite weak hooks using Hook Formula from best practices
   - Suggest shortening or expanding to optimal range
   - Recommend adding/removing hashtags
   - Propose stronger CTAs or engagement questions
   - Identify opportunities for thread expansion

4. **Reference `references/twitter-x-best-practices-2025.md`** for:
   - Algorithm understanding (first hour critical)
   - Content strategy (3-Bucket Strategy)
   - Engagement best practices

**Example workflow:**
```
User: "Review this tweet: I just launched my new productivity app. It helps you manage tasks better. Check it out!"

Assistant analysis:
- Character count: 98 (✅ optimal range!)
- Issues identified:
  * Weak hook (no attention grab)
  * No emotional connection
  * Generic language ("better", "check it out")
  * No specific value proposition
  * Missing engagement trigger

Suggested rewrite:
"Spent 200 hours building an app that cut my task management time by 70%.

Now I finish my todo list by lunch instead of midnight.

Who else drowns in tasks daily? 🙋‍♂️"

Improvements:
- Strong hook with specific numbers (200 hours, 70%)
- Emotional connection (relatable struggle)
- Clear benefit (finish by lunch vs midnight)
- Engagement trigger (question + emoji)
- 96 characters (optimal range)
```

---

### 3. Profile Optimization

Guide users through optimizing their Twitter/X profile for maximum impact and discoverability.

**When to use:**
- User asks about profile setup or optimization
- User wants to improve their bio
- User requests profile review or audit

**How to assist:**

1. **Use the comprehensive checklist** from `assets/profile-optimization-checklist.md`:
   - Profile picture quality and clarity
   - Header image (1500×500 px)
   - Username/handle searchability
   - Bio optimization with keywords
   - Pinned tweet strategy
   - Website link

2. **Apply bio optimization formula**:
   ```
   Niche + What You Do + Value You Provide + CTA
   ```
   Examples from checklist:
   - "🚀 SaaS Growth Marketer | Helping startups scale from 0-100K MRR | Ex-Google | DM for consulting"
   - "📝 Writing about productivity & AI tools | 50K+ helping creators work smarter | Newsletter ⬇️"

3. **Profile SEO guidance**:
   - Include searchable keywords in bio
   - Use relevant niche terms
   - Add location if applicable
   - Ensure consistency across platforms

4. **Pinned tweet strategy**:
   - Best viral content (social proof)
   - Introduction thread (for new visitors)
   - Current offer/project
   - High-value resource

**Example workflow:**
```
User: "Help me optimize my Twitter profile. I'm a freelance web developer."

Assistant actions:
1. Read assets/profile-optimization-checklist.md
2. Ask clarifying questions:
   - Who's your target audience? (startups, agencies, individuals?)
   - What's your main value proposition?
   - What technologies/frameworks do you specialize in?
   - Do you have social proof (projects completed, clients served)?
3. Suggest optimized bio:
   "💻 Full-Stack Developer | React/Node specialist | Built 50+ web apps for startups | Free consultation ⬇️"
4. Recommend:
   - Professional headshot as profile pic
   - Header: Screenshots of best projects
   - Pinned tweet: Case study or testimonial thread
   - Website link to portfolio
```

---

### 4. Strategy Consulting

Provide strategic guidance on content strategy, growth tactics, and audience building based on 2025 algorithm insights.

**When to use:**
- User asks about growth strategy or how to gain followers
- User wants to understand the X algorithm
- User requests content calendar or posting strategy
- User asks about engagement tactics

**How to assist:**

1. **Assess current situation**:
   - Current follower count and engagement rate
   - Posting frequency and consistency
   - Niche and target audience
   - Goals (growth, engagement, monetization)

2. **Provide algorithm insights** from `references/twitter-x-best-practices-2025.md`:
   - **The 70/30 Rule**: Spend 70% time engaging, 30% creating
   - **First hour critical**: Early engagement determines algorithmic boost
   - **Engagement hierarchy**: Replies/retweets > likes
   - **Smaller accounts favored**: 2025 updates help lesser-known creators
   - **Quality over quantity**: 3-15 quality posts beat 30 mediocre ones

3. **Recommend posting strategy**:
   - **Frequency**: Minimum 3/day, ideal 15/day, max effective 30/day
   - **Timing**: Tuesday-Thursday, 9-11 AM or 1-3 PM EST
   - **3-Bucket Strategy**:
     * 30-40% Authority content (expertise, insights)
     * 30-40% Personality content (stories, opinions)
     * 20-30% Shareability content (viral-worthy, valuable)

4. **Growth tactics**:
   - **Micro-communities**: Build group of 10-15 peers for mutual support
   - **Strategic engagement**: Reply to larger accounts in first hour
   - **Micro-influencers**: Partner with smaller, engaged creators
   - **Trending topics**: Jump on real-time trends strategically
   - **Thread strategy**: 7-10 tweets, visual breaks every 3-4 tweets

5. **Engagement best practices**:
   - Add value in replies (not "Great post!")
   - Quote tweet with insights
   - Build genuine relationships
   - Avoid self-promotion in replies

**Example workflow:**
```
User: "I've been posting daily for 3 months but only have 200 followers. What am I doing wrong?"

Assistant actions:
1. Reference references/twitter-x-best-practices-2025.md for diagnosis
2. Ask diagnostic questions:
   - How much time do you spend engaging vs creating?
   - What's your engagement rate on posts?
   - Are you using the 3-Bucket Strategy?
   - When are you posting?
3. Likely issues:
   - Probably spending 90% time creating, 10% engaging (reverse this!)
   - May be posting at wrong times
   - Content might lack emotional connection
   - Not building micro-community
4. Provide action plan:
   - Implement 70/30 rule immediately
   - Build micro-community of 10-15 peers in niche
   - Post 3-5 high-quality tweets daily at optimal times
   - Focus on Authority + Personality content
   - Engage heavily in first hour after posting
   - Track improvement over next 30 days
```

---

## Workflow Decision Tree

Use this to determine which capability to activate:

```
User request about Twitter/X?
│
├─ "Write" / "Create" / "Draft" / "Help me write"
│  └─> Capability 1: Tweet & Thread Writing
│     ├─ Single tweet? → Use assets/tweet-templates.md
│     └─ Thread? → Use assets/thread-templates.md
│
├─ "Review" / "Feedback" / "Improve" / "Is this good"
│  └─> Capability 2: Content Review & Optimization
│     ├─ Run scripts/tweet_analyzer.py
│     └─ Provide specific improvements
│
├─ "Profile" / "Bio" / "Setup" / "Optimize profile"
│  └─> Capability 3: Profile Optimization
│     └─ Use assets/profile-optimization-checklist.md
│
└─ "Strategy" / "Growth" / "Algorithm" / "How to grow"
   └─> Capability 4: Strategy Consulting
      └─ Reference references/twitter-x-best-practices-2025.md
```

---

## Resources

### scripts/

**tweet_analyzer.py**: Python script to analyze tweets for character count, engagement potential, and optimization suggestions.

Usage:
```bash
# Analyze a standard tweet
python scripts/tweet_analyzer.py "Your tweet text here"

# Analyze for Premium account (25K char limit)
python scripts/tweet_analyzer.py "Your tweet text here" --premium
```

Provides:
- Character count vs limit (280 or 25,000)
- Optimal length assessment (71-100 chars)
- Hashtag count (recommends 2-3)
- Mention and URL detection
- Engagement indicators (questions, CTAs, emojis)
- Actionable suggestions for improvement

### references/

**twitter-x-best-practices-2025.md**: Comprehensive 11,000+ word guide covering:
- Profile optimization strategies
- Platform limitations and constraints (character limits, posting frequency, media requirements)
- Content strategy and writing principles (3-Bucket Strategy, Hook Formula, content formats)
- Viral post templates (threads and single tweets)
- Algorithm understanding (ranking signals, 2025 updates, first hour rule)
- Audience growth tactics (70/30 rule, posting schedule, engagement tactics)
- Engagement best practices
- Quick reference checklists

Load this reference when users need:
- In-depth algorithm insights
- Detailed strategy guidance
- Specific platform constraints
- Comprehensive best practices
- Statistical insights (engagement rates, optimal times, etc.)

### assets/

**tweet-templates.md**: Ready-to-use templates for single tweets:
- List Format
- Story Format
- Insight Format
- Question Format
- Tool/Resource List
- Hook Formula (4-part)
- Personal Experience
- Myth-Busting
- Before/After
- Character optimization tips
- Engagement triggers
- Timing recommendations

**thread-templates.md**: Ready-to-use templates for threads:
- Classic Thread Structure (7-10 tweets)
- Storytelling Thread
- Educational Thread
- Contrarian Thread
- How-To Thread
- Listicle Thread
- Personal Journey Thread
- Hook examples and best practices
- Visual strategy guidance
- Timing and engagement tactics

**profile-optimization-checklist.md**: Comprehensive profile audit checklist:
- Profile picture guidelines
- Header image specifications (1500×500 px)
- Username and handle best practices
- Bio optimization formula with examples
- Pinned tweet strategy
- Profile SEO tactics
- Visual brand consistency
- Trust signals
- Common mistakes to avoid
- Profile refresh schedule
- Examples for different creator types

---

## Best Practices for Using This Skill

### Always Start With:
1. **Understand the user's goal**: Growth? Engagement? Monetization?
2. **Identify their niche**: Who's their target audience?
3. **Assess their current situation**: Follower count? Posting frequency?

### Key Principles:
- **Quality over quantity**: Better to write 3 great tweets than 10 mediocre ones
- **Engagement > Creation**: Emphasize the 70/30 rule
- **Emotion drives virality**: Content must make people feel something
- **First hour is critical**: Stress importance of early engagement
- **Authenticity wins**: Encourage genuine connections over tactics

### Common User Mistakes to Address:
1. Posting without engaging (breaking 70/30 rule)
2. Weak hooks that don't grab attention
3. Generic content without emotional connection
4. Wrong posting times (missing peak hours)
5. Too many or too few hashtags
6. No clear call-to-action
7. Inconsistent posting schedule

### Measurement and Iteration:
- Encourage users to track what works
- Suggest A/B testing different formats
- Recommend analyzing top-performing tweets
- Emphasize learning from engagement data
- Iterate based on results

---

## Key Insights to Share

When helping users, emphasize these critical 2025 insights:

1. **X is one of the easiest platforms to grow** because the algorithm is transparent
2. **The 70/30 Rule is non-negotiable**: 70% engaging, 30% creating
3. **Smaller accounts can win**: 2025 algorithm updates favor lesser-known creators
4. **First 60 minutes determines fate**: Early engagement = algorithmic boost
5. **Optimal length exists**: 71-100 characters get 17% higher engagement
6. **Video is 10x more powerful**: Tweets with video get 10x more engagement
7. **Quality beats quantity**: Algorithm penalizes spam now
8. **Replies > Likes**: Engagement hierarchy matters
9. **X is a café, not a billboard**: Build relationships, not just content
10. **Consistency compounds**: Daily value beats viral moments

---

## Example Interactions

### Example 1: Writing a Tweet
```
User: "Help me write a tweet about my new course launch"

Assistant:
1. Read assets/tweet-templates.md for tweet formats
2. Ask clarifying questions:
   - "What's your course about?"
   - "Who's your target audience?"
   - "What's the main benefit they'll get?"
3. Suggest Story Format or Hook Formula
4. Draft tweet:

   "I spent 6 months creating a course that teaches React in 30 days.

   Just launched it at 50% off for early adopters.

   Who's ready to finally master React? 🚀"

5. Run tweet_analyzer.py:
   - 98 characters (✅ optimal range)
   - Has question (✅ engagement)
   - Has emoji (✅)
   - Clear value prop (✅)
6. Suggest posting time: Tuesday 10 AM EST
7. Recommend: Add image of course landing page
```

### Example 2: Profile Optimization
```
User: "Review my profile bio: Tech enthusiast | Love coding | Building stuff"

Assistant:
1. Read assets/profile-optimization-checklist.md
2. Analyze current bio:
   - Too vague ("tech enthusiast", "building stuff")
   - No value proposition
   - No niche specificity
   - No social proof or credentials
3. Ask: "What do you specifically build? Who do you help? Any metrics to share?"
4. Suggest optimized version:
   "💻 Full-Stack Developer | React + Node specialist | Built 30+ apps for SaaS startups | Open source contributor"
5. Improvements:
   - Specific tech stack
   - Clear niche (SaaS startups)
   - Social proof (30+ apps)
   - Professional positioning
```

### Example 3: Strategy Question
```
User: "Why am I not growing? I post 5 times a day."

Assistant:
1. Reference references/twitter-x-best-practices-2025.md
2. Ask diagnostic questions:
   - "How much time do you spend engaging vs creating?"
   - "What's your engagement rate?"
   - "When do you post?"
3. Likely diagnosis:
   - Breaking the 70/30 rule (posting too much, engaging too little)
   - Quality over quantity issue
   - Possibly posting at wrong times
4. Provide action plan:
   - Cut posts to 3-5 high-quality tweets daily
   - Spend 2 hours daily engaging (replies, quote tweets)
   - Build micro-community of 10-15 peers
   - Post at optimal times (Tue-Thu, 9-11 AM EST)
   - Focus on emotional connection in content
   - Track engagement rate for 30 days
```

---

## Notes

- Always prioritize user's specific niche and audience
- Adapt templates to user's voice and style
- Emphasize authenticity over formulaic content
- Balance data-driven insights with creative expression
- Encourage experimentation and iteration
- Stress the importance of the 70/30 rule
- Remind that growth takes time and consistency
